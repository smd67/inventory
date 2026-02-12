<!--
This file is the vue component implementation for an other items detail screen.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Notes for {{ itemName }}
        </div>
      </v-row>  
    </v-container>
    <v-container class="table-container">
      <v-row>
        <v-data-table
          :headers="notesHeaders"
          :items="notesTable"
          :search="notesSearch"
          item-value="date"
          class="elevation-1"
          :key="notesKey"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="notesSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="addNote">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="deleteNote(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
          <template v-slot:item.description="{ item }">
            <div class="pre-wrap-cell">
              {{ item.description }}
            </div>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container class="table-container">
      <div class="d-flex justify-center align-center" style="padding-top: 20px;">
        <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
      </div>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import ConfirmDialog from './ConfirmDialog.vue';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const errorDialog = ref(null);
  const loading = ref(true);
  const itemRef = ref(null);
  const itemType = ref(null);
  const itemName = ref(null);
  const router = useRouter();
  const route = useRoute();
  const notesTable = ref([]);
  const notesSearch = ref('');
  const notesKey = ref(0);
  const confirmDialog = ref(null);
  
  // Table headers
  const notesHeaders = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  // Properties passed in to component
  const props = defineProps({
    item_ref: {
      type: Number,
      default: "",
    },
    item_type: {
      type: String,
      default: "",
    },
    item_name: {
      type: String,
      default: "",
    }
  });
  
  // fetch the user information when params change
  watch(
    // fetch the user information when params change
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN Notes.watch.refresh newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if((oldFullPath.includes("/prototype") || oldFullPath.includes("/base-unit")) && newFullPath.includes("/view-notes")){
        itemRef.value = props.item_ref;
        itemType.value = props.item_type;
        itemName.value = props.item_name;
        fetchNotes();
        notesKey.value += 1;
      } else if(oldFullPath.includes("/add-note") && newFullPath.includes("/view-notes")){ 
        fetchNotes();
        notesKey.value += 1;
      }
      console.log("OUT Notes.watch.refresh");
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN Notes.onMounted');
    itemRef.value = props.item_ref;
    itemType.value = props.item_type;
    itemName.value = props.item_name;
    fetchNotes();
    console.log('OUT Notes.onMounted itemRef=' + itemRef.value + '; itemType=' + itemType.value);
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN Notes.goBack");
    router.back();
    console.log("OUT Notes.goBack");
  };

  // Add a note to the database
  const addNote = () => {
    console.log("IN Notes.addNote");
    router.push({name: 'add-note', params: {item_type: itemType.value, item_ref: itemRef.value, item_name: itemName.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT Notes.addNote");
  }

  // Delete a note from the database
  const deleteNote = async (item) => {
    console.log("IN Notes.deleteNote item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this note?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
      };
      try {
          const response = await api.post('/delete-note', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting note:' + e,
            { color: 'red lighten-3' }
          );
      }
      console.log('Note deleted!');
      fetchNotes();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT Notes.deleteNote");
  };

  // Retrieve notes from the database through a REST call.
  const fetchNotes = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: itemType.value,
      item_ref: itemRef.value,
    };
    try {
        const response = await api.post('/get-notes', requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error fetching data. body=' + JSON.stringify(requestBody) + '; exception=' + e,
          { color: 'red lighten-3' }
        );
    }
  };
</script>

<style>
  .v-data-table {
    border: 1px solid green;
  }

  /* Set header background color */
  .theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
    background: var(--v-primary-base); /* Use a CSS variable for theme color */
  }

  /* Set alternating row colors (striped table) */
  .v-table tbody tr:nth-child(odd) {
    background-color: #f5f5f5; /* Light grey for odd rows */
  }
  .v-table thead th {
    background-color:  #F5F5DC; /* White for even rows */
  }
  .v-table tbody tr:nth-child(even) {
    background-color: #ffffff; /* White for even rows */
  }
</style>
<style scoped>
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }
  .detail-container {
    border: 1px solid green;
    width: 70%;
  }

  .detail-sheet { 
    width: 95%;
  }

  .table-container { 
    width: 80%;
  }

  .outer-div {
    width: 80%;
    padding-top: 30px;
  }

  .pre-wrap-cell {
    white-space: pre-wrap; /* or pre-line */
  }

   /* Specific styles for screens smaller than 600px */
  @media (max-width: 600px) {
    .detail-container {
      border: 1px solid green;
      width: 100%; /* Take up full width on mobile */
      padding: 0 1em; /* Add some padding */
    }
    .detail-sheet { 
      width: 99%
    }
    .table-container { 
      width: 100%
    }
    .outer-div {
      width: 100%;
    }
  }
</style>
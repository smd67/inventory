<!--
This file is the vue component implementation of a screen to add a note to the 
database. 
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px;">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Add a Note
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form @submit.prevent="handleSubmit">
            <v-text-field
              v-model="description"
              label="Description"
            ></v-text-field>
            <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
            </div>
          </v-form>
        </v-sheet>
      </v-row>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const loading = ref(true);
  const description = ref(null);
  const itemType = ref(null);
  const itemRef = ref(0);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);

  // Properties passed into component
  const props = defineProps({
    item_ref: {
      type: Number,
      default: 0,
    },
    item_type : {
      type: String,
      default: "",
    },
  });

  // Resets data when path changes
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN AddNote.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if(newFullPath.includes("/add-note")){
        itemType.value = props.item_type;
        itemRef.value = props.item_ref;
        description.value = null;
      }
      console.log('OUT AddNote.watch.refresh. itemType=' + itemType.value + '; itemRef=' + itemRef.value);
    }
  );

  // Initialize data on component mount
  onMounted(async () => {
    console.log('IN AddNote.onMounted');
    itemType.value = props.item_type;
    itemRef.value = props.item_ref;
    description.value = null;
    console.log('OUT AddNote.onMounted. itemType=' + itemType.value + '; itemRef=' + itemRef.value);
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN goBack");
    router.back()
    console.log("OUT goBack");
  }

  // This method handles the REST call to insert the note into the database.
  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        description: description.value,
        item_type: itemType.value,
        item_ref: itemRef.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/add-note', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.error('Error inserting data:', e);
        // Call the dialog's open function using the template ref
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error inserting data:' + e,
          { color: 'red lighten-3' }
        );
    }
    goBack();
    console.log('OUT handleSubmit');
  };
</script>
<style scoped>
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
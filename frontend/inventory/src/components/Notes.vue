<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 150px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Notes
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error">
    <v-container>
      <!-- Data Table -->
      <v-data-table
        :headers="headers"
        :items="notesTable"
        :search="search"
        item-value="date"
        class="elevation-1"
      >
        <!-- If you still want the default pagination controls alongside the search -->
        <template v-slot:footer.prepend>
          <v-text-field
            v-model="search"
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
        </template>
      </v-data-table>
    </v-container>
    <div class="d-flex justify-center align-center">
      <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
    </div>
  </div>
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps } from 'vue';
  import axios from 'axios';
  import { VDataTable } from 'vuetify/components';
  import { useRouter } from 'vue-router';
  import api from "../api";

  const search = ref('')
  const notesTable = ref([]);
  const error = ref(null);
  const loading = ref(true);
  const item_type = ref(null);
  const item_ref = ref(0);
  const router = useRouter();
  const headers = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true}
  ]);

  const props = defineProps({
    item_type: {
      type: String,
      default: "",
    },
    item_ref: {
      type: Number,
      default: 0,
    },
  });

  onMounted(async () => {
    console.log('IN onMounted');
    item_type.value = props.item_type;
    item_ref.value = props.item_ref;
    fetchNotes();
    console.log('OUT onMounted');
  });

  const goBack = () => {
    console.log("IN goBack");
    router.push({name: 'prototype'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT goBack");
  }

  const fetchNotes = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: item_type.value,
      item_ref: item_ref.value,
    };
    console.log("body=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/get-notes/', requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

</script>

<style>
  .v-data-table {
    border: 5px solid green;
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
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }
</style>
<!--
This file is the vue component implementation to create a base unit object 
in the database.
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
          Create a Base Unit
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form @submit.prevent="handleSubmit">
            <v-text-field
              v-model="name"
              label="Name"
              :key="nameKey"
            ></v-text-field>
            <v-text-field
              v-model="location"
              label="Location"
              :key="locationKey"
            ></v-text-field>
            <v-checkbox
              v-model="has_new_feet"
              label="Has new feet?"
              :key="hasNewFeetKey"
            ></v-checkbox>
            <v-checkbox
              v-model="has_new_mast_bearing"
              label="Has new mast bearing?"
              :key="hasNewMastBearingKey"
            ></v-checkbox>
            <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
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
  import { ref, onMounted, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const errorDialog = ref(null);
  const loading = ref(true);
  const name = ref(null);
  const location = ref(null);
  const has_new_feet = ref(false);
  const has_new_mast_bearing = ref(false);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const locationKey = ref(0);
  const hasNewFeetKey = ref(0);
  const hasNewMastBearingKey = ref(0);

  // Watcher to reset data when path changes
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN Create.watch.refresh");
      name.value = null;
      nameKey.value += 1;
      location.value = null;
      locationKey.value += 1;
      has_new_feet.value = false;
      hasNewFeetKey.value += 1;
      has_new_mast_bearing.value = false;
      hasNewMastBearingKey.value += 1;
      console.log("OUT Create.watch.refresh");
    }
  );

  // Initilize when component mounts
  onMounted(async () => {
    console.log('IN onMounted');
    console.log('OUT onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Submit the REST call to create a new base unit
  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        name: name.value,
        location: location.value,
        has_new_mast_bearing: has_new_mast_bearing.value,
        has_new_feet: has_new_feet.value,
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/create-base-unit', requestBody, config);
        console.log("status=" + response.status);
        activity_log('Base Unit', 
                     name.value, 
                     "Created Base Unit: " + name.value + 
                     " at location=" + location.value +
                     ", has_new_mast_bearing=" + has_new_mast_bearing.value +
                     ", has_new_feet=" + has_new_feet.value);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        // Call the dialog's open function using the template ref
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error inserting data:' + e,
          { color: 'red lighten-3' }
        );
        console.error('Error fetching data:', e);
    }
    goBack();
    console.log('OUT handleSubmit');
  };
</script>
<style scoped>
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
<!--
This file is the vue component implementation to create a camera object 
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
          Create a Camera
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
            <v-select
              v-model="cameraType"
              :items="cameraTypes"
              label="Camera Type"
              :key="cameraTypeKey"
            ></v-select>
            <v-select
              v-model="baseUnit"
              :items="baseUnitNames"
              label="Base Unit (optional)"
              :key="baseUnitKey"
            ></v-select>
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
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Properties passed into component
  const props = defineProps({
    base_unit: {
      type: String,
      default: null,
    }
  });

  // Data
  const loading = ref(true);
  const name = ref(null);
  const baseUnit = ref(null);
  const baseUnitNames = ref(null);
  const cameraType = ref(null)
  const cameraTypes = ref(['Face Camera', 'License Plate Camera', 'Wide Screen Camera', 'Other']);
  const router = useRouter();
  const route = useRoute();
  const baseUnitKey = ref(0);
  const nameKey = ref(0);
  const cameraTypeKey = ref(0);
  const errorDialog = ref(null);

  // Watcher to reset data when path changes
  watch(
    () => [route.params.base_unit],
    async refresh => {
      console.log("IN CreateCamera.watch.refresh");
      baseUnit.value = props.base_unit;
      baseUnitKey.value += 1;
      name.value = null;
      nameKey.value += 1;
      cameraType.value = null;
      cameraTypeKey.value += 1;
      fetchBaseUnitNames();
      console.log("OUT CreateCamera.watch.refresh");
    }
  );

  // Initialize data on component load
  onMounted(async () => {
    console.log('IN onMounted');
    baseUnit.value = props.base_unit;
    baseUnitKey.value += 1;
    name.value = null;
    nameKey.value += 1;
    cameraType.value = null;
    cameraTypeKey.value += 1;
    fetchBaseUnitNames();
    console.log('OUT onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Handle REST call to create a camera object in the database.
  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        name: name.value,
        camera_type: cameraType.value,
        base_unit: baseUnit.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/create-camera', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
        let logStr = "Created Camera: " + name.value + 
                      ", type=" + cameraType.value;
        if(baseUnit.value != null) {
          logStr +=  ", base_unit=" + baseUnit.value;
          activity_log('Base Unit', 
                       baseUnit.value, 
                       'Added Camera ' + name.value + ' to Base Unit ' + baseUnit.value);
        }
        activity_log('Camera', name.value, logStr);
        
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

  // Retrieve base units from the database.
  const fetchBaseUnitNames = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-base-units-names', config);
        baseUnitNames.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching data:' + e,
            { color: 'red lighten-3' }
          );
    }
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
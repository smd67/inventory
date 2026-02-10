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
          Add a Camera
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form @submit.prevent="handleSubmit">
            <v-select
              v-model="cameraType"
              :items="cameraTypes"
              label="Camera Type"
            ></v-select>
            <v-select
              v-model="camera"
              :items="camerasByType"
              item-title="name"
              item-value="name"
              label="Camera"
            ></v-select>
            <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Add</v-btn>
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
  import { ref, onMounted, defineProps, watch, computed } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Properties passed into component
  const props = defineProps({
    base_unit_id: {
      type: Number,
      default: null,
    },
    base_unit_name: {
      type: String,
      default: null,
    },
  });

  // Data
  const loading = ref(true);
  const baseUnitRef = ref(null);
  const baseUnitName = ref(null);
  const camera = ref(null);
  const availableCameras = ref([]);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);
  const cameraType = ref('All')
  const cameraTypes = ref(['Face Camera', 'License Plate Camera', 'Wide Screen Camera', 'Other', 'All']);

  // Watcher to reset data when path changes
  watch(
    () => [route.params.id, route.params.base_unit_name],
    async refresh => {
      console.log("IN AddCamera.watch.refresh");
      baseUnitRef.value = props.base_unit_id;
      baseUnitName.value = props.base_unit_name;
      camera.value = ref(null);
      cameraType.value = 'All';
      fetchAvailableCameras();
      console.log("OUT AddCamera.watch.refresh");
    }
  );

  // Initialize data on component load
  onMounted(async () => {
    console.log('IN AddCamera.onMounted');
    baseUnitRef.value = props.base_unit_id;
    baseUnitName.value = props.base_unit_name;
    camera.value = ref(null);
    cameraType.value = 'All';
    fetchAvailableCameras();
    console.log('OUT AddCamera.onMounted. baseUnitRef=' + baseUnitRef.value + ', baseUnitName=' + baseUnitName.value);
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN AddCamera.goBack");
    router.back();
    console.log("OUT AddCamera.goBack");
  };

  // Retrieve base units from the database.
  const fetchAvailableCameras = async () => {
    console.log("IN AddCamera.fetchAvailableCameras");
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    try {
        const response = await api.get('/get-available-cameras', config);
        availableCameras.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching data:' + e,
            { color: 'red lighten-3' }
          );
    }
    console.log("OUT AddCamera.fetchAvailableCameras. availableCameras=" + availableCameras.value);
  };

  const camerasByType = computed(() => {
    console.log("IN AddCamera.camerasByType. type=" + cameraType.value);
    let cameraList = [];

    if(cameraType.value === 'All'){
      cameraList = availableCameras.value;
    } else {
      cameraList = availableCameras.value.filter(item => {return item.type == cameraType.value;});
    }
    console.log("OUT AddCamera.camerasByType. cameraList=" + JSON.stringify(cameraList));
    if(cameraList.length > 0){
      camera.value = cameraList[0].name;
    } else {
      camera.value = '';
    }
    
    return cameraList;
  });

  // Handle REST call to update a camera object in the database.
  // Submit updates to database through a REST call.
  const handleSubmit = async () => {
    console.log('IN handleSubmit camera=' + camera.value + '; baseUnitName=' + baseUnitName.value);
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    console.log("camera=" + JSON.stringify(camera.value));
    const requestBody = {
        name: camera.value,
        base_unit: baseUnitName.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/update-camera', requestBody, config);
        console.log("status=" + response.status);
        activity_log('Base Unit', 
                     baseUnitName.value, 
                     'Adding camera ' + camera.value + ' to Base Unit ' + baseUnitName.value);
        activity_log('Camera', 
                     camera.value, 
                     'Added to Base Unit ' + baseUnitName.value);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.error('Error updating data:', e);
        // Call the dialog's open function using the template ref
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error updating data:' + e,
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
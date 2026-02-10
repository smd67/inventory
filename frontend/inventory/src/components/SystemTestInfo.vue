<!--
This file is the vue component implementation of a screen to gather information
prior to performing a system test checklist.
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
          Information for System Test Checklist
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-text-field
            v-model="technicianName"
            label="Technician Name"
          ></v-text-field>
          <v-select
            v-model="baseUnit"
            :items="baseUnitNames"
            label="Base Unit"
          ></v-select>
          <v-date-input v-model="reportDate" label="Report Date"></v-date-input>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;"  @click="goNext">Next</v-btn>
          </div>
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
  import { VDateInput } from 'vuetify/labs/VDateInput'
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const loading = ref(true);
  const technicianName = ref(null);
  const reportDate = ref(null);
  const baseUnit = ref(null);
  const baseUnitNames = ref(null);
  const faceCameras = ref([]);
  const licensePlateCameras = ref([]);
  const widescreenCameras = ref([]);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);
  
  // Watch method to reset cached data 
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN SystemTestInfo.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if(oldFullPath.includes("/prototype")){
        technicianName.value = null;
        reportDate.value = new Date().toISOString().slice(0, 10);
        baseUnit.value = null;
      }
      fetchBaseUnitNames();
      console.log('OUT SystemTestInfo.watch.refresh');
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN SystemTestInfo.onMounted');
    technicianName.value = null;
    reportDate.value = new Date().toISOString().slice(0, 10);
    baseUnit.value = null;
    fetchBaseUnitNames();
    console.log("OUT SystemTestInfo.onMounted");
  });

  // Method to return to the previous page.
  const goBack = () => {
    console.log("IN SystemTestInfo.goBack");
    router.back()
    console.log("OUT SystemTestInfo.goBack");
  }

  const goNext = async () => {
    console.log("IN SystemTestInfo.goNext");
    await fetchBaseUnitByName();
    router.push({
      name: "system-test-checklist", 
      params: {technician_name: technicianName.value, base_unit: baseUnit.value, report_date: reportDate.value },
      query: { face_cameras: faceCameras.value, license_plate_cameras: licensePlateCameras.value, widescreen_cameras: widescreenCameras.value }
    });
    console.log("OUT SystemTestInfo.goNext");
  }

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
  const fetchBaseUnitByName = async () => {
    console.log("IN SystemTestInfo.fetchBaseUnitByName: baseUnit=" + baseUnit.value);

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      name: baseUnit.value,
    };
    try {
        const response = await api.post('/get-base-unit-by-name', requestBody, config);
        const target_bu = response.data;
        faceCameras.value = target_bu.face_cameras;
        licensePlateCameras.value = target_bu.license_plate_cameras;
        widescreenCameras.value = target_bu.widescreen_cameras;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching other-items:' + e,
            { color: 'red lighten-3' }
          );
    }
    console.log("OUT SystemTestInfo.fetchBaseUnitByName faceCameras=" + JSON.stringify(faceCameras.value) + "; licensePlateCameras=" + JSON.stringify(licensePlateCameras.value) + "; widescreenCameras=" + JSON.stringify(widescreenCameras.value));
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
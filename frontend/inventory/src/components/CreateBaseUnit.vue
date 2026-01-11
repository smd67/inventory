<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 225px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Create a Base Unit
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error" style="padding-right: 250px;">
    <v-container style="border: 1px solid green" width="700">
      <v-sheet class="pa-4 text-right" width="600">
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
          <v-text-field
            v-model="face_camera"
            label="Face Camera (optional)"
            :key="faceCameraKey"
          ></v-text-field>
          <v-text-field
            v-model="license_plate_camera"
            label="License Plate Camera (optional)"
            :key="licensePlateCameraKey"
          ></v-text-field>
           <v-text-field
            v-model="widescreen_camera"
            label="Widescreen Camera (optional)"
            :key="widescreenCameraKey"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-container>
  </div>
  
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, watch } from 'vue';
  import axios from 'axios';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";

  const error = ref(null);
  const loading = ref(true);
  const name = ref(null);
  const location = ref(null);
  const has_new_feet = ref(false);
  const has_new_mast_bearing = ref(false);
  const face_camera = ref(null);
  const license_plate_camera = ref(null);
  const widescreen_camera = ref(null);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const locationKey = ref(0);
  const hasNewFeetKey = ref(0);
  const hasNewMastBearingKey = ref(0);
  const faceCameraKey = ref(0);
  const licensePlateCameraKey = ref(0);
  const widescreenCameraKey = ref(0);

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
      face_camera.value = null;
      faceCameraKey.value += 1;
      license_plate_camera.value = null;
      licensePlateCameraKey.value += 1;
      widescreen_camera.value = null;
      widescreenCameraKey.value += 1;
      console.log("OUT Create.watch.refresh");
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    console.log('OUT onMounted');
  });

  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

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
        face_camera: face_camera.value,
        license_plate_camera: license_plate_camera.value,
        widescreen_camera: widescreen_camera.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/create-base-unit/', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
        console.error('Error fetching data:', e);
    }
    goBack();
    console.log('OUT handleSubmit');
  };
</script>
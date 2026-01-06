<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 225px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Add an Asset
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error" style="padding-right: 250px;">
    <v-container style="border: 1px solid green" width="700">
      <v-sheet class="pa-4 text-right" width="600">
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="id"
            :rules="rules"
            label="ID"
          ></v-text-field>
          <v-text-field
            v-model="location"
            :rules="rules"
            label="Location"
          ></v-text-field>
          <v-checkbox
            v-model="has_new_feet"
            label="Has new feet?"
          ></v-checkbox>
          <v-checkbox
            v-model="has_new_mast_bearing"
            label="Has new mast bearing?"
          ></v-checkbox>
          <v-text-field
            v-model="together_with_face_camera"
            :rules="rules"
            label="With Face Camera"
          ></v-text-field>
          <v-text-field
            v-model="together_with_license_plate_camera"
            :rules="rules"
            label="With License Plate Camera"
          ></v-text-field>
           <v-text-field
            v-model="together_with_widescreen_camera"
            :rules="rules"
            label="With Widescreen Camera"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
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
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

  const error = ref(null);
  const loading = ref(true);
  const id = ref(null);
  const location = ref(null);
  const has_new_feet = ref(false);
  const has_new_mast_bearing = ref(false);
  const together_with_face_camera = ref(null);
  const together_with_license_plate_camera = ref(null);
  const together_with_widescreen_camera = ref(null);
  const router = useRouter();

  onMounted(async () => {
    console.log('IN onMounted');
    console.log('OUT onMounted');
  });

  const goBack = () => {
    console.log("IN goBack");
    router.push({name: 'prototype'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT goBack");
  }

  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const apiUrl = 'http://127.0.0.1:8001/create-asset/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        id: id.value,
        location: location.value,
        has_new_feet: has_new_feet.value,
        has_new_mast_bearing: has_new_mast_bearing.value,
        together_with_face_camera: together_with_face_camera.value,
        together_with_license_plate_camera: together_with_license_plate_camera.value,
        together_with_widescreen_camera: together_with_widescreen_camera.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await axios.post(apiUrl, requestBody, config);
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
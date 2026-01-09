<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 225px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Create a Camera
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
          ></v-text-field>
          <v-select
            v-model="cameraType"
            :items="cameraTypes"
            label="Camera Type"
          ></v-select>
          <v-text-field
            v-model="baseUnit"
            label="Base Unit (optional)"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
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
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from "../api";

  const error = ref(null);
  const loading = ref(true);
  const name = ref(null);
  const baseUnit = ref(null);
  const cameraType = ref(null)
  const cameraTypes = ref(['Face Camera', 'License Plate Camera', 'Wide Screen Camera', 'Other']);
  const router = useRouter();

  onMounted(async () => {
    console.log('IN onMounted');
    console.log('OUT onMounted');
  });

  const goBack = () => {
    console.log("IN goBack");
    router.push({ path: '/prototype' });
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
        camera_type: cameraType.value,
        base_unit: baseUnit.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/create-camera/', requestBody, config);
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
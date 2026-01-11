<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 12.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Create a Camera
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div style="padding-right: 25%;">
    <v-container style="border: 1px solid green" width="70%">
      <v-sheet class="pa-4 text-right" width="95%">
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
          <v-text-field
            v-model="baseUnit"
            label="Base Unit (optional)"
            :key="baseUnitKey"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  const props = defineProps({
    base_unit: {
      type: String,
      default: null,
    }
  });

  const loading = ref(true);
  const name = ref(null);
  const baseUnit = ref(null);
  const cameraType = ref(null)
  const cameraTypes = ref(['Face Camera', 'License Plate Camera', 'Wide Screen Camera', 'Other']);
  const router = useRouter();
  const route = useRoute();
  const baseUnitKey = ref(0);
  const nameKey = ref(0);
  const cameraTypeKey = ref(0);
  const errorDialog = ref(null);

  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN CreateCamera.watch.refresh");
      baseUnit.value = props.base_unit;
      baseUnitKey.value += 1;
      name.value = null;
      nameKey.value += 1;
      cameraType.value = null;
      cameraTypeKey.value += 1;
      console.log("OUT CreateCamera.watch.refresh");
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    baseUnit.value = props.base_unit;
    baseUnitKey.value += 1;
    name.value = null;
    nameKey.value += 1;
    cameraType.value = null;
    cameraTypeKey.value += 1;
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
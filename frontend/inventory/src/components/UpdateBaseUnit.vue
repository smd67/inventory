<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 22.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Update Camera
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
            readonly
          ></v-text-field>
          <v-text-field
            v-model="location"
            :key="locationKey"
            label="Location"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
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
    name: {
      type: String,
      default: null,
    },
    id: {
      type: Number,
      default: -1,
    },
  });

  const loading = ref(true);
  const name = ref(null);
  const id = ref(null);
  const location = ref(null);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const locationKey = ref(0);
  const errorDialog = ref(null);

  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN UpdateBaseUnit.watch.refresh");
      name.value = props.name;
      nameKey.value += 1;
      location.value = null;
      locationKey.value += 1;
      id.value = props.id;
      console.log("OUT UpdateBaseUnit.watch.refresh");
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    name.value = props.name;
    nameKey.value += 1;
    id.value = props.id;
    location.value = null;
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
        id: id.value,
        name: name.value,
        location: location.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/update-base-unit/', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.error('Error updating data:', e);
        // Call the dialog's open function using the template ref
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error updating base unit:' + e,
          { color: 'red lighten-3' }
        );
    }
    goBack();
    console.log('OUT handleSubmit');
  };
</script>
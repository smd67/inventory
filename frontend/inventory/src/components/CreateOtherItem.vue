<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 17.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Create an Other Item
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div style="padding-right: 250px;">
    <v-container style="border: 1px solid green" width="60%">
      <v-sheet class="pa-4 text-right" width="95%">
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="name"
            label="Name"
          ></v-text-field>
          <v-text-field
            v-model="baseUnit"
            label="Base Unit (optional)"
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
  import { ref, onMounted, defineProps } from 'vue';
  import { useRouter } from 'vue-router';
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
  const router = useRouter();
  const errorDialog = ref(null);

  onMounted(async () => {
    console.log('IN onMounted');
    baseUnit.value = props.base_unit;
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
        base_unit: baseUnit.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/create-other-item/', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.error('Error updating data:', e);
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
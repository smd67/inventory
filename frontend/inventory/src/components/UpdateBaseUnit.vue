<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 22.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Update Base Unit
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="detail-container">
      <v-sheet class="pa-4 text-right detail-sheet">
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
          <v-checkbox
            v-model="hasNewFeet"
            label="Has new feet?"
            :key="hasNewFeetKey"
          ></v-checkbox>
          <v-checkbox
            v-model="hasNewMastBearing"
            label="Has new mast bearing?"
            :key="hasNewMastBearingKey"
          ></v-checkbox>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
  </div>  
</template>

<script setup>
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';
  import ConfirmDialog from './ConfirmDialog.vue';

  const props = defineProps({
    name: {
      type: String,
      default: null,
    },
    id: {
      type: Number,
      default: -1,
    },
    location: {
      type: String,
      default: null,
    },
    has_new_feet: {
      type: Boolean,
      default: false
    },
    has_new_mast_bearing: {
      type: Boolean,
      default: false
    },
  });

  const loading = ref(true);
  const name = ref(null);
  const id = ref(null);
  const location = ref(null);
  const hasNewFeet = ref(null);
  const hasNewMastBearing = ref(null);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const locationKey = ref(0);
  const hasNewFeetKey = ref(0);
  const hasNewMastBearingKey = ref(0);
  const errorDialog = ref(null);
  const confirmDialog = ref(null);

  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN UpdateBaseUnit.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      name.value = props.name;
      nameKey.value += 1;
      location.value = null;
      locationKey.value += 1;
      id.value = props.id;
      hasNewFeet.value = props.has_new_feet;
      hasNewFeetKey.value += 1;
      hasNewMastBearing.value = props.has_new_mast_bearing;
      hasNewMastBearingKey.value += 1;
      console.log("OUT UpdateBaseUnit.watch.refresh");
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    name.value = props.name;
    nameKey.value += 1;
    location.value = props.location;
    locationKey.value += 1;
    id.value = props.id;
    hasNewFeet.value = props.has_new_feet;
    hasNewFeetKey.value += 1;
    hasNewMastBearing.value = props.has_new_mast_bearing;
    hasNewMastBearingKey.value += 1;
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
        location: location.value,
        has_new_feet: hasNewFeet.value,
        has_new_mast_bearing: hasNewMastBearing.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const result = await confirmDialog.value.open(
          'Confirm Update',
          'Are you sure you want to update this base unit?',
          { color: 'red lighten-3' }
        );

        if (result) {
          const response = await api.post('/update-base-unit', requestBody, config);
          console.log("status=" + response.status);
          loading.value = false;
        }
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

<style>
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
    padding-right: 25%;
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
      padding-right: 0%;
    }
  }
</style>
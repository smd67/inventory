<!--
This file is the vue component implementation for a screen that updates a base
unit.
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
          Update Base Unit
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
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
            <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Submit</v-btn>
            </div>
          </v-form>
        </v-sheet>
      </v-row>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
  </div>  
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';
  import ConfirmDialog from './ConfirmDialog.vue';

  // Properties passe in to component.
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
    }
  });

  // Data
  const loading = ref(true);
  const name = ref(null);
  const id = ref(null);
  const location = ref(null);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const locationKey = ref(0);
  const errorDialog = ref(null);
  const confirmDialog = ref(null);

  // A watcher to reset data when the path changes.
  watch(
    () => [route.params.name, route.params.id, route.params.location],
    async refresh => {
      console.log("IN UpdateBaseUnit.watch.refresh");
      name.value = props.name;
      nameKey.value += 1;
      location.value = props.location;
      locationKey.value += 1;
      id.value = props.id;
      console.log("OUT UpdateBaseUnit.watch.refresh");
    }
  );

  // Initialize data when component mounts.
  onMounted(async () => {
    console.log('IN UpdateBaseUnit.onMounted');
    name.value = props.name;
    nameKey.value += 1;
    location.value = props.location;
    locationKey.value += 1;
    id.value = props.id;
    console.log("location=" + location.value + "; props.location=" + props.location);
    console.log('OUT UpdateBaseUnit.onMounted.');
  });

  // Go back to previous page.
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Submit the changes to the database through a REST call.
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
        const result = await confirmDialog.value.open(
          'Confirm Update',
          'Are you sure you want to update this base unit?',
          { color: 'red lighten-3' }
        );

        if (result) {
          const response = await api.post('/update-base-unit', requestBody, config);
          console.log("status=" + response.status);

          if(props.location !== location.value){
            activity_log('Base Unit', 
                          name.value, 
                          "Location changed from: " + props.location +
                          " to: " + location.value);
          }
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
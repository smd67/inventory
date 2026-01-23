<!--
This file is the vue component implementation for a screen that updates an
other item.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="detail-container">
      <v-row>
        <div style="color: green; font-size: 24px;">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Update Other Item
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
              v-model="baseUnit"
              :key="baseUnitKey"
              label="Base Unit"
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
  </div>  
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Properties passed in to component
  const props = defineProps({
    name: {
      type: String,
      default: null,
    }
  });

  // Data
  const loading = ref(true);
  const name = ref(null);
  const baseUnit = ref(null);
  const router = useRouter();
  const route = useRoute();
  const nameKey = ref(0);
  const baseUnitKey = ref(0);
  const errorDialog = ref(null);

  // A watcher that resets data when the full path changes.
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN UpdateOtherItem.watch.refresh");
      baseUnit.value = props.base_unit;
      baseUnitKey.value += 1;
      name.value = props.name;
      nameKey.value += 1;
      baseUnit.value = null;
      baseUnitKey.value += 1;
      console.log("OUT UpdateOtherItem.watch.refresh");
    }
  );

  // Initialize data when component is mounted.
  onMounted(async () => {
    console.log('IN onMounted');
    name.value = props.name;
    nameKey.value += 1;
    console.log('OUT onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Submit changes to database through a REST call.
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
        const response = await api.post('/update-other-item', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
        if(props.base_unit != baseUnit.value){
            activity_log('Base Unit', 
                          baseUnit.value, 
                          "Other Item " + name.value + " moved to Base Unit " + baseUnit.value);
            activity_log('Other Item', 
                          name.value, 
                          "Moved to Base Unit " + baseUnit.value);
        }
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
<!--
This file is the vue component implementation to create a otherItem object 
to a base unit.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px;">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Add an Other Item
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form @submit.prevent="handleSubmit">
            <v-select
              v-model="otherItem"
              :items="availableOtherItems"
              item-title="name"
              item-value="name"
              label="Other Item"
            ></v-select>
            <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" type="submit">Add</v-btn>
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
  import { ref, onMounted, defineProps, watch, computed } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Properties passed into component
  const props = defineProps({
    base_unit_id: {
      type: Number,
      default: null,
    },
    base_unit_name: {
      type: String,
      default: null,
    },
  });

  // Data
  const loading = ref(true);
  const baseUnitRef = ref(null);
  const baseUnitName = ref(null);
  const otherItem = ref(null);
  const availableOtherItems = ref([]);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);
  
  // Watcher to reset data when path changes
  watch(
    () => [route.params.base_unit_id, route.params.base_unit_name],
    async refresh => {
      console.log("IN AddOtherItem.watch.refresh");
      baseUnitRef.value = props.base_unit_id;
      baseUnitName.value = props.base_unit_name;
      otherItem.value = null;
      await fetchAvailableOtherItems();
      console.log("OUT AddOtherItem.watch.refresh");
    }
  );

  // Initialize data on component load
  onMounted(async () => {
    console.log('IN AddOtherItem.onMounted');
    baseUnitRef.value = props.base_unit_id;
    baseUnitName.value = props.base_unit_name;
    otherItem.value = null;
    await fetchAvailableOtherItems();
    console.log('OUT AddOtherItem.onMounted. baseUnitRef=' + baseUnitRef.value + ', baseUnitName=' + baseUnitName.value);
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN AddOtherItem.goBack");
    router.back();
    console.log("OUT AddOtherItem.goBack");
  };

  // Retrieve base units from the database.
  const fetchAvailableOtherItems = async () => {
    console.log("IN AddOtherItem.fetchAvailableOtherItems");
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    try {
        const response = await api.get('/get-available-other-items', config);
        availableOtherItems.value = response.data;
        if(availableOtherItems.value.length > 0){
          otherItem.value = availableOtherItems.value[0].name;
        } else {
          otherItem.value = '';
        }
        loading.value = false;
    } catch (e) {
        loading.value = false;
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching data:' + e,
            { color: 'red lighten-3' }
          );
    }
    console.log("OUT AddOtherItem.fetchAvailableOtherItems. availableOtherItems=" + availableOtherItems.value);
  };


  // Handle REST call to create a otherItem object in the database.
  // Submit updates to database through a REST call.
  const handleSubmit = async () => {
    console.log('IN handleSubmit otherItem=' + otherItem.value + '; baseUnitName=' + baseUnitName.value);
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    console.log("otherItem=" + JSON.stringify(otherItem.value));
    const requestBody = {
        name: otherItem.value,
        base_unit: baseUnitName.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/update-other-item', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
        activity_log('Base Unit', 
                     baseUnitName.value, 
                     'Adding Other Item ' + otherItem.value + ' to Base Unit ' + baseUnitName.value);
        activity_log('Other Item', 
                     otherItem.value, 
                     'Added to Base Unit ' + baseUnitName.value);
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
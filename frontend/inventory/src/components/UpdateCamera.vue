<!--
This file is the vue component implementation for a screen that updates a 
camera.
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
          Update Camera
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
            <v-select
              v-model="lane"
              :items="laneIndicators"
              label="Lane"
              :key="laneKey"
            ></v-select>
            <v-select
              v-model="baseUnit"
              :items="baseUnitNames"
              label="Base Unit"
            ></v-select>
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
  import api, {activity_log, fetchBaseUnitNames} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Properties passed in to the component
  const props = defineProps({
    name: {
      type: String,
      default: null,
    },
    lane: {
      type: String,
      default: null,
    },
    base_unit_name: {
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
  const baseUnitNames = ref([]);
  const lane = ref('NONE');
  const laneIndicators = ref([]);
  const errorDialog = ref(null);

  // A watcher that updates data when the path changes.
   watch(
    () => [route.params.name, route.params.base_unit_name],
    async refresh => {
      console.log("IN UpdateCamera.watch.refresh");
      baseUnit.value = props.base_unit;
      baseUnitKey.value += 1;
      name.value = props.name;
      lane.value = props.lane;
      nameKey.value += 1;
      baseUnit.value = props.base_unit_name;
      baseUnitKey.value += 1;
      baseUnitNames.value = await fetchBaseUnitNames();
      await fetchLaneIndicators();
      console.log("OUT UpdateCamera.watch.refresh");
    }
  );

  // Initialize data when component is mounted.
  onMounted(async () => {
    console.log('IN UpdateCamera.onMounted');
    name.value = props.name;
    lane.value = props.lane;
    nameKey.value += 1;
    baseUnit.value = props.base_unit_name;
    baseUnitKey.value += 1;
    baseUnitNames.value = await fetchBaseUnitNames();
    await fetchLaneIndicators();
    console.log('OUT UpdateCamera.onMounted. baseUnit.value=' + baseUnit.value + "; props.base_unit_name=" +  props.base_unit_name);
  });

  // Go back to previous page.
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Submit updates to database through a REST call.
  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        name: name.value,
        lane: lane.value,
        base_unit: baseUnit.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/update-camera', requestBody, config);
        console.log("status=" + response.status);
        loading.value = false;
        if(props.base_unit != baseUnit.value){
            let cameraName = name.value;
            if(lane.value !== 'NONE'){
              cameraName += "[" + lane.value + "]";
            }
            if(!Object.is(baseUnit.value, null)){
              activity_log('Base Unit', 
                            baseUnit.value, 
                            "Camera " + cameraName + " moved to Base Unit " + baseUnit.value);
              activity_log('Camera', 
                            cameraName, 
                            "Moved to Base Unit " + baseUnit.value);
            }
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
  // Retrieve lane indicator values.
  const fetchLaneIndicators = async () => {
    const config = {
      headers: {
          'Content-Type': 'application/json'
      }
    };

    try {
      const response = await api.get('/get-camera-lane-indicators', config);
      laneIndicators.value = response.data;
      loading.value = false;
    } catch (e) {
      loading.value = false;
      const result = await errorDialog.value.open(
          'Confirm Error',
          'Error fetching data:' + e,
          { color: 'red lighten-3' }
        );
    }
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
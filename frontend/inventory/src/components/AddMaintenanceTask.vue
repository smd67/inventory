<!--
This file is the vue component implementation of a screen to add a maintenance 
task to the database. 
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
          Add Maintenance Task for {{ itemName }}
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form @submit.prevent="handleSubmit">
            <v-text-field
              v-model="description"
              label="Description"
            ></v-text-field>
            <v-text-field
              v-model="technicianName"
              label="Technician Name"
            ></v-text-field>
            <v-date-input v-model="dueDate" label="Due Date"></v-date-input>
            <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
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
  import { VDateInput } from 'vuetify/labs/VDateInput'
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const loading = ref(true);
  const description = ref(null);
  const itemType = ref(null);
  const itemRef = ref(0);
  const itemName = ref(null);
  const dueDate = ref(null);
  const technicianName = ref(null);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);

  // Properties
  const props = defineProps({
    item_ref: {
      type: Number,
      default: 0,
    },
    item_type : {
      type: String,
      default: "",
    },
    item_name : {
      type: String,
      default: "",
    }
  });

  const itemTypeMap = {
    "BASE_UNIT": "Base Unit",
    "CAMERA": "Camera",
    "OTHER": "Other Item"
  };

  // Watch method to reset cached data 
  watch(
    () => [route.params.item_ref, route.params.item_type, route.params.item_name],
    async refresh => {
      console.log("IN AddMaintenanceTask.watch.refresh");
      itemType.value = props.item_type;
      itemRef.value = props.item_ref;
      itemName.value = props.item_name;
      description.value = null;
      dueDate.value = new Date().toISOString().slice(0, 10);;
      technicianName.value = null;
      console.log('OUT AddMaintenanceTask.watch.refresh. itemType=' + itemType.value + '; itemRef=' + itemRef.value);
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN AddMaintenaceTask.onMounted');
    itemType.value = props.item_type;
    itemRef.value = props.item_ref;
    itemName.value = props.item_name;
    dueDate.value = new Date().toISOString().slice(0, 10);;
    technicianName.value = null;
    console.log('OUT AddMaintenaceTask.onMounted. itemType=' + itemType.value + '; itemRef=' + itemRef.value);
  });

  // Method to return to the previous page.
  const goBack = () => {
    console.log("IN goBack");
    router.back()
    console.log("OUT goBack");
  }

  // This method handles the REST call to insert the maintenance task.
  const handleSubmit = async () => {
    console.log('IN handleSubmit');
    const config = {
      headers: {
          'Content-Type': 'application/json'
      }
    };
    const requestBody = {
      due_date: dueDate.value,
      description: description.value,
      item_type: itemType.value,
      item_ref: itemRef.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/add-maintenance-task', requestBody, config);
        console.log("status=" + response.status);
        activity_log(itemTypeMap[itemType.value], 
                     itemName.value, 
                     "Maintenance task opened: " + description.value,
                     technicianName.value);
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
<style scoped>
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
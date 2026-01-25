<!--
This file is the vue component implementation for a screen that updates a 
maintenance task by "completing" it, meaning the last done stamp is set to
the current time.
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
          Update Maintenance Task
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-text-field
            v-model="description"
            label="Description of Task"
            :key="descriptionKey"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="technicianName"
            label="Technician Name"
          ></v-text-field>
          <v-date-input
            v-model="dueDate" 
            label="New Due Date"
            :key="dueDateKey"
          ></v-date-input>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" @click="completeTask">Complete</v-btn>
          </div>
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
  import { VDateInput } from 'vuetify/labs/VDateInput'

  // Properties passed in to component.
  const props = defineProps({
    id: {
      type: Number,
      default: null,
    },
    description: {
      type: String,
      default: null,
    },
    item_type: {
      type: String,
      default: null,
    },
    item_name: {
      type: String,
      default: null,
    },
  });

  // Data
  const loading = ref(true);
  const id = ref(null);
  const description = ref(null);
  const dueDate = ref(null);
  const itemType = ref(null);
  const itemName = ref(null);
  const technicianName = ref(null);
  const router = useRouter();
  const route = useRoute();
  const descriptionKey = ref(0);
  const dueDateKey = ref(0);
  const errorDialog = ref(null);
  const confirmDialog = ref(null);

  // Watcher that resets data when the routing path changes.
  watch(
      () => [route.params.id, route.description, route.params.item_type,  route.params.item_name],
      async refresh => {
        console.log("IN UpdateMaintenanceTask.watch.refresh");
        description.value = props.description;
        descriptionKey.value += 1;
        dueDate.value = new Date().toISOString().slice(0, 10);
        dueDateKey.value += 1;
        id.value = props.id;
        itemType.value = props.item_type;
        itemName.value = props.item_name;
        technicianName.value = null;
        console.log('OUT UpdateMaintenanceTask.watch.refresh. id=' + id.value + '; description=' + description.value);
    }
  );

  // Initialize data when component is moounted.
  onMounted(async () => {
    console.log('IN UpdateMaintenanceTask.onMounted');
    id.value = props.id;
    itemType.value = props.item_type;
    itemName.value = props.item_name;
    description.value = props.description;
    descriptionKey.value += 1;
    dueDate.value = new Date().toISOString().slice(0, 10);
    dueDateKey.value += 1;
    technicianName.value = null;
    console.log('OUT UpdateMaintenanceTask.onMounted');
  });

  // Go back to previous page.
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  // Complete the task by updating the last done stamp to now.
  const completeTask = async () => {
    console.log('IN completeTask');
    const result = await confirmDialog.value.open(
      'Confirm Completion',
      'Are you sure that you have completed this task?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
          headers: {
              'Content-Type': 'application/json'
          }
      };
      const requestBody = {
          id: id.value,
          due_date: dueDate.value
      };
      console.log("requestBody=" + JSON.stringify(requestBody));
      try {
          const response = await api.post('/complete-maintenance-task', requestBody, config);
          console.log("status=" + response.status);
          loading.value = false;
          activity_log(itemType.value, 
                      itemName.value, 
                      "Maintenance task completed. Description - " + description.value + ". By - " + technicianName.value,
                      technicianName.value);
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
    }
    goBack();
    console.log('OUT completeTask');
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
<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 22.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Update Maintenance Task
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div style="padding-right: 25%;">
    <v-container style="border: 1px solid green" width="70%">
      <v-sheet class="pa-4 text-right" width="95%">
        <v-text-field
          v-model="description"
          label="Description"
          :key="descriptionKey"
          readonly
        ></v-text-field>
        <v-text-field
          v-model="lastDoneDate"
          :key="lastDoneDateKey"
          label="Last Done Date"
          readonly
        ></v-text-field>
        <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;" @click="completeTask">Complete</v-btn>
        </div>
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
    id: {
      type: Number,
      default: null,
    },
    description: {
      type: String,
      default: null,
    },
    last_done_date: {
      type: String,
      default: null
    }
  });

  const loading = ref(true);
  const id = ref(null);
  const description = ref(null);
  const lastDoneDate = ref(null);
  const router = useRouter();
  const route = useRoute();
  const descriptionKey = ref(0);
  const lastDoneDateKey = ref(0);
  const errorDialog = ref(null);
  const confirmDialog = ref(null);

  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN UpdateMaintenanceTask.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if(newFullPath.includes("/update-maintenance-task")){
        description.value = props.description;
        descriptionKey.value += 1;
        lastDoneDate.value = props.last_done_date;
        lastDoneDateKey.value += 1;
        id.value = props.id;
      }
      console.log('OUT UpdateMaintenanceTask.watch.refresh. id=' + id.value + '; description=' + description.value);
    }
  );

  onMounted(async () => {
    console.log('IN UpdateMaintenanceTask.onMounted');
    id.value = props.id;
    description.value = props.description;
    descriptionKey.value += 1;
    lastDoneDate.value = props.last_done_date;
    lastDoneDateKey.value += 1;
    console.log('OUT UpdateMaintenanceTask.onMounted');
  });

  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  }

  const completeTask = async () => {
    console.log('IN completeTask');
    const result = await confirmDialog.value.open(
      'Confirm Completion',
      'Are you sure you want to complete this task?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
          headers: {
              'Content-Type': 'application/json'
          }
      };
      const requestBody = {
          id: id.value
      };
      console.log("requestBody=" + JSON.stringify(requestBody));
      try {
          const response = await api.post('/complete-maintenance-task/', requestBody, config);
          console.log("status=" + response.status);
          loading.value = false;
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
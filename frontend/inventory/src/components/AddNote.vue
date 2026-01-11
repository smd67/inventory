<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 22.5%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Add a Note
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div style="padding-right: 25%;">
    <v-container style="border: 1px solid green" width="70%">
      <v-sheet class="pa-4 text-right" width="95%">
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="description"
            label="Description"
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
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

  const loading = ref(true);
  const description = ref(null);
  const itemType = ref(null);
  const itemRef = ref(0);
  const router = useRouter();
  const errorDialog = ref(null);

  const props = defineProps({
    item_ref: {
      type: Number,
      default: 0,
    },
    item_type : {
      type: String,
      default: "",
    },
  });

  onMounted(async () => {
    console.log('IN AddMaintenaceTask.onMounted');
    itemType.value = props.item_type;
    itemRef.value = props.item_ref;
    console.log('OUT AddMaintenaceTask.onMounted. itemType=' + itemType.value + '; itemRef=' + itemRef.value);
  });

  const goBack = () => {
    console.log("IN goBack");
    router.back()
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
        description: description.value,
        item_type: itemType.value,
        item_ref: itemRef.value
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/add-note/', requestBody, config);
        console.log("status=" + response.status);
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
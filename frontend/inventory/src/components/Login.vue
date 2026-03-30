<template>
    <v-container class="table-container">
        <v-row>
            <div style="color: green; font-size: 24px">
                <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
                Login
            </div>
        </v-row>  
        <v-row style="padding-top: 50px;">
            <v-form @submit.prevent="login"  style="width: 80%;">
                <!--
                <input type="text" v-model="username" placeholder="Username" class="form-object" style="background-color: lightgray;"/>
                <input type="password" v-model="password" placeholder="Password" class="form-object" style="background-color: lightgray;"/>
                -->
                <v-row>
                    <v-col cols="12" md="4">
                        <v-text-field
                            v-model="username"
                            label="Username"
                            prepend-icon="mdi-account"
                            variant="outlined"
                            density="compact"
                            hide-details
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                        <v-text-field
                            v-model="password"
                            label="Password"
                            type="password"
                            prepend-icon="mdi-lock"
                            variant="outlined"
                            density="compact"
                            hide-details
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                        <v-btn type="submit" outlined> Submit </v-btn>
                    </v-col>
                </v-row>
            </v-form>
        </v-row>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
</template>


<script setup>
  // Imports
  import { ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const errorDialog = ref(null);
  const username = ref(null);
  const password = ref(null);
  const router = useRouter();
  const login = async () => {

    try {
        const config = {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        };
        console.log("Encode ...");
        // 2. Encode to Base64
        const encodedUser = btoa(username.value);
        const encodedPass = btoa(password.value);

        console.log("Create search params ...");
        // 3. Prepare data using URLSearchParams
        const params = new URLSearchParams();
        params.append('username', encodedUser);
        params.append('password', encodedPass);

        console.log("Send request ...");
        const response = await api.post('/login', params, config);

        console.log("Route ...");
        router.push({name: 'prototype'}).catch(failure => {
            console.log('An unexpected navigation failure occurred:', failure);
        });
    } catch (err) {
        console.log("error=" + err)
        const result = await errorDialog.value.open(
          'Login Error',
          'Username or Password incorrect. Please check your credentials and try again',
          { color: 'red lighten-3' }
        );
    }
}
</script>

<style scoped>
    .my-button {
        cursor: pointer;
        padding: 8px 20px;
        border: 1px solid transparent;
        border-radius: 6px; /* */
        font-weight: 700;
    }
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

    .pre-wrap-cell {
        white-space: pre-wrap; /* or pre-line */
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
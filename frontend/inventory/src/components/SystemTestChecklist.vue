<!--
This file is the vue component implementation for a report that lists all 
maintenance tasks whose last due date is >= 6 months.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Asset Tracker
        </div>
      </v-row>
      <v-row>
        <v-col>
          <v-card>
            <v-toolbar color="#4F9153" density="compact" :elevation="8" title="System Test Checklist">
            </v-toolbar>

            <div class="d-flex flex-row">
              <v-tabs v-model="activeTab" bg-color="#F5F5DC" direction="vertical">
                <v-tab text="General" value="general_tab"></v-tab>
                <v-tab
                  v-for="item in faceCameras"
                  :text="`Face Camera - ${item}`"
                  :value="`face_camera_tab_${item }`"
                >
                </v-tab>
              
                <v-tab
                  v-for="item in licensePlateCameras"
                  :text="`License Plate Camera - ${item}`"
                  :value="`license_plate_camera_tab_${item }`"
                >
                </v-tab>

                <v-tab
                  v-for="item in widescreenCameras"
                  :text="`Widescreen Camera - ${item}`"
                  :value="`widescreen_camera_tab_${item }`"
                >
                </v-tab>

                <v-tab
                  v-for="item in widescreenCameras"
                  :text="`LiDar - ${item}`"
                  :value="`lidar_tab_${item }`"
                >
                </v-tab>

                <v-tab text="Boom" value="boom_tab"></v-tab>
                <v-tab
                  v-for="item in widescreenCameras"
                  :text="`Widescreen Actuators - ${item}`"
                  :value="`widescreen_actuators_tab_${item }`"
                >
                </v-tab>

                <v-tab text="Radar" value="radar_tab"></v-tab>
                <v-tab text="Wind Meter" value="wind_meter_tab"></v-tab>
                <v-tab text="Mast" value="mast_tab"></v-tab>
              </v-tabs>
              <v-tabs-window v-model="activeTab">
                <v-tabs-window-item value="general_tab">
                  <v-card flat v-if="activeTab === 'general_tab'">
                    <v-card-text>
                      <!-- Checkbox Group in Tab 1 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in generalCheckbox"
                          v-model="generalItems"
                          :label="item.label"
                          :value="item.value"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                
                <v-tabs-window-item 
                  v-for="top_item in faceCameras" 
                  :value="`face_camera_tab_${top_item}`"
                >
                  <v-card flat v-if="activeTab === `face_camera_tab_${top_item}`">
                    <v-card-text>
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in faceCameraCheckbox" 
                          v-model="faceCameraItems"
                          :label="item.label"
                          :value="`${item.value}_${top_item}`"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                
                
                <v-tabs-window-item 
                  v-for="top_item in licensePlateCameras" 
                  :value="`license_plate_camera_tab_${top_item }`"
                >
                  <v-card flat v-if="activeTab === `license_plate_camera_tab_${top_item}`">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 3 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in licensePlateCameraCheckbox"
                          v-model="licensePlateCameraItems"
                          :label="item.label"
                          :value="`${item.value}_${top_item}`"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>


                <v-tabs-window-item 
                  v-for="top_item in widescreenCameras"
                  :value="`widescreen_camera_tab_${top_item}`"
                >
                  <v-card flat v-if="activeTab === `widescreen_camera_tab_${top_item}`">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 4 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in widescreenCameraCheckbox"
                          v-model="widescreenCameraItems"
                          :label="item.label"
                          :value="`${item.value}_${top_item}`"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item 
                  v-for="top_item in widescreenCameras"
                  :value="`lidar_tab_${top_item}`"
                 >
                  <v-card flat v-if="activeTab === `lidar_tab_${top_item}`">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 5 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in liDarCheckbox"
                          v-model="liDarItems"
                          :label="item.label"
                          :value="`${item.value}_${top_item}`"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item value="boom_tab">
                  <v-card flat v-if="activeTab === 'boom_tab'">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 2 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in boomCheckbox"
                          v-model="boomItems"
                          :label="item.label"
                          :value="item.value"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item 
                  v-for="top_item in widescreenCameras"
                  :value="`widescreen_actuators_tab_${top_item}`"
                >
                  <v-card flat v-if="activeTab === `widescreen_actuators_tab_${top_item}`">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 7 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in widescreenActuatorsCheckbox"
                          v-model="widescreenActuatorsItems"
                          :label="item.label"
                          :value="`${item.value}_${top_item}`"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item value="radar_tab">
                  <v-card flat v-if="activeTab === 'radar_tab'">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 8 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in radarCheckbox"
                          v-model="radarItems"
                          :label="item.label"
                          :value="item.value"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item value="wind_meter_tab">
                  <v-card flat v-if="activeTab === 'wind_meter_tab'">
                    <v-card-text>
                      <!-- Another Checkbox Group in Tab 9 -->
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in windMeterCheckbox"
                          v-model="windMeterItems"
                          :label="item.label"
                          :value="item.value"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item value="mast_tab">
                  <v-card flat v-if="activeTab === 'mast_tab'">
                    <v-card-text>
                      <div class="checkbox-grid">
                        <!-- Another Checkbox Group in Tab 10 -->
                        <v-checkbox
                          v-for="item in mastCheckBox"
                          v-model="mastItems"
                          :label="item.label"
                          :value="item.value"
                          class="grid-item"
                        ></v-checkbox>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
              </v-tabs-window>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">
            Back
          </v-btn>
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="handleSubmit">
            Submit
          </v-btn>
        </div>
        <v-spacer></v-spacer>
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
    import api from "../api";
    import ErrorDialog from './ErrorDialog.vue';
    import ConfirmDialog from './ConfirmDialog.vue';

    const generalCheckbox = ref([
      {id: 1, label: "12V and 24V power supplies are active", value: "power_supplies_active"},
      {id: 2, label: "Jetson is powered by 12V", value: "jetson_is_powered"},
      {id: 3, label: "Cerbo is powered", value: "cerbo_is_powered"},
      {id: 4, label: "Switch and modem are functioning", value: "switch_and_modem_functioning"},
      {id: 5, label: "Switch in top mast box is functioning", value: "switch_in_top_mast_functioning"},

    ]);
    const faceCameraCheckbox = ref([
      {id: 1, label: "At least one fan is working", value: "at_least_one_fan_working"},
      {id: 2, label: "8 LEDs are working", value: "leds_are_working"},
      {id: 3, label: "Camera gets more than 8 AvgFPS", value: "gets_more_than_8_AvgFPS"},
      {id: 4, label: "Camera IP is set for ..1.5 (or ..1.8 if 2 lane)", value: "camera_ip_is_properly_set"},
      {id: 5, label: "Camera triggers by script trigger", value: "triggered_by_script"},
      {id: 6, label: "LED is flashing by script trigger", value: "led_is_flashing_by_script_trigger"},
      {id: 7, label: "Focus is working", value: "focus_is_working"},
      {id: 8, label: "Focus is not slipping", value: "focus_is_not_slipping"},
      {id: 9, label: "Focus value 180 == Infinity on lens", value: "focus_value_180_equals_infinity_on_lens"},
      {id: 10, label: "Focus set to 180", value: "focus_set_to_180"},
    ]);
    const licensePlateCameraCheckbox = ref([
      {id: 1, label: "At least one fan is working", value: "at_least_one_fan_working", model: "licensePlateCameraItems"},
      {id: 2, label: "Camera gets more than 8 AvgFPS", value: "gets_more_than_8_AvgFPS", model: "licensePlateCameraItems"},
      {id: 3, label: "Camera IP is set for ..1.4 (or ..1.7 if 2 lane)", value: "ip_is_correct", model: "licensePlateCameraItems"},
      {id: 4, label: "Camera triggers by script trigger", value: "triggered_by_script", model: "licensePlateCameraItems"},
      {id: 5, label: "Focus is working", value: "focus_is_working", model: "licensePlateCameraItems"},
      {id: 6, label: "Focus is not slipping", value: "focus_is_not_slipping", model: "licensePlateCameraItems"},
      {id: 7, label: "Focus value 180 == Infinity on lens", value: "focus_value_180_equals_infinity_on_lens", model: "licensePlateCameraItems"},
      {id: 8, label: "Focus set to 180", value: "focus_set_to_180", model: "licensePlateCameraItems"},
    ]);
    const widescreenCameraCheckbox = ref([
      {id: 1, label: "at least one fan is working", value: "fan_is_working"},
      {id: 2, label: "8 LEDs are working", value: "leds_are_working"},
      {id: 3, label: "Camera gets more than 8 AvgFPS", value: "camera_gets_more_than_8_avgFPS"},
      {id: 4, label: "Camera IP is set for ..1.6 (or ..1.9 if 2 lane)", value: "camera_ip_is_correct"},
      {id: 5, label: "Camera triggers by script trigger", value: "camera_triggered_by_script"},
      {id: 6, label: "Focus is working", value: "focus_is_working"},
      {id: 7, label: "Focus is not slipping", value: "focus_is_not_slipping"},
      {id: 8, label: "Focus value 180 == Infinity on lens", value: "focus_value_180_equals_infinity_on_lens"},
      {id: 9, label: "Focus set to 180", value: "focus_set_to_180"},
    ]);
    const liDarCheckbox = ref([
      {id: 1, label: "Can read value by minicom", value: "can_read_value_by_minicom"},
      {id: 2, label: "Can range the distance", value: "can_range_the_distance"},
      {id: 3, label: "Programm direction set to:  entry == 1", value: "programm_direction_set"},
      {id: 4, label: "Programm LaserPointer set to:  off == 0", value: "programm_laser_pointer_set"},
      {id: 5, label: "Programm Blank set to: 7.00m", value: "programm_blank_set"},
      {id: 6, label: "Programm DetectMode set to: detect == 1", value: "programm_detect_mode_set"},
    ]);
    const boomCheckbox = ref([
      {id: 1, label: "Rotation is functioning", value: "boom_rotation_functioning"},
      {id: 2, label: "Has new mast bearing", value: "boom_has_new_mast_bearing"},
      {id: 3, label: "Rotates Out to the limit", value: "boom_rotates_out_to_limit"},
      {id: 4, label: "Rotates In to the limit", value: "boom_rotates_in_to_limit"},
      {id: 5, label: "Extension is functioning", value: "boom_extension_is_functioning"},
      {id: 6, label: "Extends Out to the limit", value: "boom_extends_out_to_limit"},
      {id: 7, label: "Extends In to the limit", value: "boom_extends_in_to_limit"},
    ])
    const widescreenActuatorsCheckbox = ref([
      {id: 1, label: "Yaw is functioning", value: "yaw_is_functioning"},
      {id: 2, label: "Roll is functioning", value: "roll_is_functioning"},
      {id: 3, label: "Pitch is functioning", value: "pitch_is_functioning"}
    ]);
    const radarCheckbox = ref([
      {id: 1, label: "Visual indication (Blue and Red LED)", value: "visual_indication_blue_and_red_led"},
      {id: 2, label: "Can connect by default IP 192.168.10.123", value: "can_connect_to_default_ip"},
      {id: 3, label: "IP set to 192.168.1.13", value: "ip_set_correctly"},
      {id: 4, label: "Height is set to 6m", value: "height_set_correctly"},
      {id: 5, label: "Angle is set around 10 degree", value: "angle_set_correctly"},
    ]);
    const windMeterCheckbox = ref([
      {id: 1, label: "RS485 adapter is functioning", value: "adapter_is_functioning"},
      {id: 2, label: "RS485 ip set to 192.168.1.17", value: "ip_set_correctly"}
    ]);
    const mastCheckBox = ref([
      {id: 1, label: "Fully extends (6.0m)", value: "mast_fully_extends"},
      {id: 2, label: "Has a mark at 6.0m", value: "mast_mark_Correct"},
      {id: 3, label: "Fully extends in", value: "mast_fully_extends_in"},
      {id: 4, label: "Manual socket is functional", value: "mast_socket_is_functional"}
    ]);

    // Properties passed into component.
  const props = defineProps({
    technician_name: {
      type: String,
      default: "",
    },
    base_unit: {
      type: String,
      default: "",
    },
    report_date: {
      type: Date,
      default: null,
    }
  });

    // Data
    const errorDialog = ref(null);
    const confirmDialog = ref(null);
    const loading = ref(true);
    const router = useRouter();
    const route = useRoute();
    const activeTab = ref('general_tab');
    const technicianName = ref(null);
    const baseUnitName = ref(null);
    const faceCameras = ref([]);
    const licensePlateCameras = ref([]);
    const widescreenCameras = ref([]);
    const reportDate = ref(null);

    // Checkbox group states 
    const generalItems = ref([]); 
    const boomItems = ref([]); 
    const faceCameraItems = ref([]); 
    const licensePlateCameraItems = ref([]);
    const widescreenCameraItems = ref([]);
    const liDarItems = ref([]);
    const widescreenActuatorsItems = ref([]);
    const radarItems = ref([]);
    const windMeterItems = ref([]);
    const mastItems = ref([]);

    // fetch the user information when params change
    // Watch method to reset cached data 
    watch(
      () => route.fullPath,
      async (newFullPath, oldFullPath) => {
        console.log("IN SystemTestChecklist.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
        if(newFullPath.includes("/system-test-checklist")){
          technicianName.value = props.technician_name;
          reportDate.value = props.date;
          baseUnitName.value = props.base_unit;
          faceCameras.value = route.query.face_cameras;
          licensePlateCameras.value = route.query.license_plate_cameras;
          widescreenCameras.value = route.query.widescreen_cameras;
        }
        console.log('OUT SystemTestChecklist.watch.refresh baseUnitName=' + baseUnitName.value + '; faceCameras=' + faceCameras.value + '; licensePlateCameras=' + licensePlateCameras.value + '; widescreenCameras=' + widescreenCameras.value);
      }
    );

    // Initialize data on component mount
    onMounted(async () => {
      console.log('IN SystemTestChecklist.onMounted');
      technicianName.value = props.technician_name;
      reportDate.value = props.date;
      baseUnitName.value = props.base_unit;
      faceCameras.value = route.query.face_cameras;
      licensePlateCameras.value = route.query.license_plate_cameras;
      widescreenCameras.value = route.query.widescreen_cameras;
      console.log('OUT SystemTestChecklist.onMounted baseUnitName=' + baseUnitName.value + '; faceCameras=' + faceCameras.value + '; licensePlateCameras=' + licensePlateCameras.value + '; widescreenCameras=' + widescreenCameras.value);
    });

  // Go back to previous page
  const goBack = () => {
    console.log("IN SystemTestChecklist.goBack");
    router.back();
    console.log("OUT SystemTestChecklist.goBack");
  };

  // Go back to previous page
  const handleSubmit = async () => {
    console.log("IN SystemTestChecklist.handleSubmit. widescreenCameraItems=" + widescreenCameraItems.value);
    const result = await confirmDialog.value.open(
      'Confirm Update',
      'Are you sure you want to submit this checklist?',
      { color: 'red lighten-3' }
    );

    console.log("OUT SystemTestChecklist.handleSubmit");
  };
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
    width: 100%;
    padding-top: 30px;
  }
  .checkbox-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Creates two equal-width columns */
    gap: 5px;
  }

  .grid-item {
    display: flex;
    align-items: center;
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
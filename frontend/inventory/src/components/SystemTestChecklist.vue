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
            <div :class="[$vuetify.display.mdAndUp ? 'd-flex flex-row' : '']">
              <v-tabs 
                v-model="activeTab" 
                bg-color="#F5F5DC" 
                :direction="$vuetify.display.mdAndUp ? 'vertical' : 'horizontal'"
                :vertical="!$vuetify.display.mdAndUp"
              >
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
                      <div class="checkbox-grid">
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
                  :key="top_item.id"
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
                          :key="item.id"
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
                          v-for="item in mastCheckbox"
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
    import api, {activity_log} from "../api";
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
    const mastCheckbox = ref([
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
      () => [route.params.technician_name, route.params.base_unit, route.params.report_date],
      async refresh => {
        console.log("IN SystemTestChecklist.watch.refresh");
        technicianName.value = props.technician_name;
        reportDate.value = props.report_date;
        baseUnitName.value = props.base_unit;
        faceCameras.value = route.query.face_cameras;
        licensePlateCameras.value = route.query.license_plate_cameras;
        widescreenCameras.value = route.query.widescreen_cameras;
        generalItems.value = []; 
        boomItems.value = []; 
        faceCameraItems.value = []; 
        licensePlateCameraItems.value = [];
        widescreenCameraItems.value = [];
        liDarItems.value = [];
        widescreenActuatorsItems.value = [];
        radarItems.value = [];
        windMeterItems.value = [];
        mastItems.value = [];
        console.log('OUT SystemTestChecklist.watch.refresh baseUnitName=' + baseUnitName.value + '; faceCameras=' + faceCameras.value + '; licensePlateCameras=' + licensePlateCameras.value + '; widescreenCameras=' + widescreenCameras.value);
      }
    );

    // Initialize data on component mount
    onMounted(async () => {
      console.log('IN SystemTestChecklist.onMounted');
      technicianName.value = props.technician_name;
      reportDate.value = props.report_date;
      baseUnitName.value = props.base_unit;
      faceCameras.value = route.query.face_cameras;
      licensePlateCameras.value = route.query.license_plate_cameras;
      widescreenCameras.value = route.query.widescreen_cameras;
      generalItems.value = []; 
      boomItems.value = []; 
      faceCameraItems.value = []; 
      licensePlateCameraItems.value = [];
      widescreenCameraItems.value = [];
      liDarItems.value = [];
      widescreenActuatorsItems.value = [];
      radarItems.value = [];
      windMeterItems.value = [];
      mastItems.value = [];
      console.log('OUT SystemTestChecklist.onMounted baseUnitName=' + baseUnitName.value + '; faceCameras=' + faceCameras.value + '; licensePlateCameras=' + licensePlateCameras.value + '; widescreenCameras=' + widescreenCameras.value);
    });

  // Go back to previous page
  const goBack = () => {
    console.log("IN SystemTestChecklist.goBack");
    router.back();
    console.log("OUT SystemTestChecklist.goBack");
  };

  const generateDialogText = () => {
    console.log("IN SystemTestChecklist.generateDialogText");
    let baseDialog = 'Are you sure you want to submit this checklist?';
    const expectedGeneral = new Set(generalCheckbox.value.map(item => item.value));
    const missingGeneral = expectedGeneral.difference(new Set(generalItems.value));
    const labelsGeneral = generalCheckbox.value.filter(item => missingGeneral.has(item.value)).map(item => item.label);
    
    let expectedFaceCameraVals = [];
    for (const camera of faceCameras.value) {
      console.log("camera=" + camera);
      const cameraVals = faceCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedFaceCameraVals = [...expectedFaceCameraVals, ...cameraVals];
    }
    const expectedFaceCamera = new Set(expectedFaceCameraVals);
    const missingFaceCamera = expectedFaceCamera.difference(new Set(faceCameraItems.value));

    let expectedLicensePlateCameraVals = [];
    for (const camera of licensePlateCameras.value) {
      const cameraVals = licensePlateCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedLicensePlateCameraVals = [...expectedLicensePlateCameraVals, ...cameraVals];
    }
    const expectedLicensePlateCamera = new Set(expectedLicensePlateCameraVals);
    const missingLicensePlateCamera = expectedLicensePlateCamera.difference(new Set(licensePlateCameraItems.value));


    let expectedWidescreenCameraVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = widescreenCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedWidescreenCameraVals = [...expectedWidescreenCameraVals, ...cameraVals];
    }
    const expectedWidescreenCamera = new Set(expectedWidescreenCameraVals);
    const missingWidescreenCamera = expectedWidescreenCamera.difference(new Set(widescreenCameraItems.value));

    let expectedLiDarVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = liDarCheckbox.value.map(item => item.value + '_' + camera);
      expectedLiDarVals = [...expectedLiDarVals, ...cameraVals];
    }
    const expectedLiDar = new Set(expectedLiDarVals);
    const missingLiDar = expectedLiDar.difference(new Set(liDarItems.value));

    let expectedWidescreenActuatorsVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = widescreenActuatorsCheckbox.value.map(item => item.value + '_' + camera);
      expectedWidescreenActuatorsVals = [...expectedWidescreenActuatorsVals, ...cameraVals];
    }
    const expectedWidescreenActuators = new Set(expectedWidescreenActuatorsVals);
    const missingWidescreenActuators = expectedWidescreenActuators.difference(new Set(widescreenActuatorsItems.value));

    const expectedBoom = new Set(boomCheckbox.value.map(item => item.value));
    const missingBoom = expectedBoom.difference(new Set(boomItems.value));
    const labelsBoom = boomCheckbox.value.filter(item => missingBoom.has(item.value)).map(item => item.label);

    const expectedRadar = new Set(radarCheckbox.value.map(item => item.value));
    const missingRadar = expectedRadar.difference(new Set(radarItems.value));
    const labelsRadar = radarCheckbox.value.filter(item => missingRadar.has(item.value)).map(item => item.label);

    const expectedWindMeter = new Set(windMeterCheckbox.value.map(item => item.value));
    const missingWindMeter = expectedWindMeter.difference(new Set(windMeterItems.value));
    const labelsWindMeter = windMeterCheckbox.value.filter(item => missingWindMeter.has(item.value)).map(item => item.label);

    const expectedMast = new Set(mastCheckbox.value.map(item => item.value));
    const missingMast = expectedMast.difference(new Set(mastItems.value));
    const labelsMast = mastCheckbox.value.filter(item => missingMast.has(item.value)).map(item => item.label);

    if(labelsGeneral.length > 0 || labelsBoom.length > 0 || labelsRadar.length > 0 || labelsWindMeter.length > 0 || labelsMast.length > 0 || missingFaceCamera.length > 0 || missingLicensePlateCamera.length > 0 || missingWidescreenCamera.length > 0|| missingLiDar.size > 0){
       baseDialog =  baseDialog + ' The following checks are missing\n';
    }
    if(labelsGeneral.length > 0){
      baseDialog =  baseDialog + '<b>General</b>: ' + labelsGeneral.join(', ') + '\n';
    }
    if(labelsBoom.length > 0){
      baseDialog =  baseDialog + '<b>Boom</b>: ' + labelsBoom.join(', ') + '\n';
    }
    if(labelsRadar.length > 0){
      baseDialog =  baseDialog + '<b>Radar</b>: ' + labelsRadar.join(', ') + '\n';
    }
    if(labelsMast.length > 0){
      baseDialog =  baseDialog + '<b>Mast</b>: ' + labelsMast.join(', ') + '\n';
    }

    if(labelsWindMeter.length > 0){
      baseDialog =  baseDialog + '<b>Wind Meter</b>: ' + labelsWindMeter.join(', ') + '\n';
    }

    if(missingFaceCamera.size > 0){
      for (const camera of faceCameras.value) {
        const missingFaceCameraList = [...missingFaceCamera];
        const missingForCamera = new Set(missingFaceCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = faceCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        baseDialog =  baseDialog + '<b>Face Camera - ' + camera + '</b>:' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingLicensePlateCamera.size > 0){
      for (const camera of licensePlateCameras.value) {
        const missingLicensePlateCameraList = [...missingLicensePlateCamera];
        const missingForCamera = new Set(missingLicensePlateCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = licensePlateCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        baseDialog =  baseDialog + '<b>License Plate Camera - ' + camera + '</b>:' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingWidescreenCamera.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingWidescreenCameraList = [...missingWidescreenCamera];
        const missingForCamera = new Set(missingWidescreenCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = widescreenCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        baseDialog =  baseDialog + '<b>Widescreen Camera - ' + camera + '</b>:' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingLiDar.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingLiDarList = [...missingLiDar];
        const missingForCamera = new Set(missingLiDarList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = liDarCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        baseDialog =  baseDialog + '<b>LiDar - ' + camera + '</b>:' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingWidescreenActuators.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingWidescreenActuatorsList = [...missingWidescreenActuators];
        const missingForCamera = new Set(missingWidescreenActuatorsList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = widescreenActuatorsCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        baseDialog =  baseDialog + '<b>Widescreen Actuators - ' + camera + '</b>:' + labelsForCamera.join(', ') + '\n';
      }
    }
    console.log("OUT SystemTestChecklist.generateDialogText. baseDialog=" + baseDialog);
    return baseDialog;
  }

  const generateMaintTasks = (descriptions, itemType, itemName, subsystem) => {
    for (const description of descriptions) {
      addMaintTask(subsystem + ': ' + description, itemType, itemName);
    }
  };

  const generateReport = (location) => {
    console.log("IN SystemTestChecklist.generateReport");

    let reportStr = 'System Test Checklist Executed\n';
    reportStr = reportStr + "=========================\n"
    reportStr =     reportStr + 'Technician Name: ' + technicianName.value + '\n';
    reportStr =     reportStr + 'Location:        ' + location + '\n';
    reportStr =     reportStr + 'Report Date:     ' + reportDate.value + '\n';
    
    const expectedGeneral = new Set(generalCheckbox.value.map(item => item.value));
    const missingGeneral = expectedGeneral.difference(new Set(generalItems.value));
    const labelsGeneral = generalCheckbox.value.filter(item => missingGeneral.has(item.value)).map(item => item.label);
    const passGeneral = new Set(generalItems.value);
    const labelsGeneralPass = generalCheckbox.value.filter(item => passGeneral.has(item.value)).map(item => item.label);

    let expectedFaceCameraVals = [];
    for (const camera of faceCameras.value) {
      const cameraVals = faceCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedFaceCameraVals = [...expectedFaceCameraVals, ...cameraVals];
    }
    const expectedFaceCamera = new Set(expectedFaceCameraVals);
    const missingFaceCamera = expectedFaceCamera.difference(new Set(faceCameraItems.value));

    let expectedLicensePlateCameraVals = [];
    for (const camera of licensePlateCameras.value) {
      const cameraVals = licensePlateCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedLicensePlateCameraVals = [...expectedLicensePlateCameraVals, ...cameraVals];
    }
    const expectedLicensePlateCamera = new Set(expectedLicensePlateCameraVals);
    const missingLicensePlateCamera = expectedLicensePlateCamera.difference(new Set(licensePlateCameraItems.value));


    let expectedWidescreenCameraVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = widescreenCameraCheckbox.value.map(item => item.value + '_' + camera);
      expectedWidescreenCameraVals = [...expectedWidescreenCameraVals, ...cameraVals];
    }
    const expectedWidescreenCamera = new Set(expectedWidescreenCameraVals);
    const missingWidescreenCamera = expectedWidescreenCamera.difference(new Set(widescreenCameraItems.value));

    let expectedLiDarVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = liDarCheckbox.value.map(item => item.value + '_' + camera);
      expectedLiDarVals = [...expectedLiDarVals, ...cameraVals];
    }
    const expectedLiDar = new Set(expectedLiDarVals);
    const missingLiDar = expectedLiDar.difference(new Set(liDarItems.value));

    let expectedWidescreenActuatorsVals = [];
    for (const camera of widescreenCameras.value) {
      const cameraVals = widescreenActuatorsCheckbox.value.map(item => item.value + '_' + camera);
      expectedWidescreenActuatorsVals = [...expectedWidescreenActuatorsVals, ...cameraVals];
    }
    const expectedWidescreenActuators = new Set(expectedWidescreenActuatorsVals);
    const missingWidescreenActuators = expectedWidescreenActuators.difference(new Set(widescreenActuatorsItems.value));

    const expectedBoom = new Set(boomCheckbox.value.map(item => item.value));
    const missingBoom = expectedBoom.difference(new Set(boomItems.value));
    const labelsBoom = boomCheckbox.value.filter(item => missingBoom.has(item.value)).map(item => item.label);
    const passBoom = new Set(boomItems.value);
    const labelsBoomPass = boomCheckbox.value.filter(item => passBoom.has(item.value)).map(item => item.label);


    const expectedRadar = new Set(radarCheckbox.value.map(item => item.value));
    const missingRadar = expectedRadar.difference(new Set(radarItems.value));
    const labelsRadar = radarCheckbox.value.filter(item => missingRadar.has(item.value)).map(item => item.label);
    const passRadar = new Set(radarItems.value);
    const labelsRadarPass = radarCheckbox.value.filter(item => passRadar.has(item.value)).map(item => item.label);

    const expectedWindMeter = new Set(windMeterCheckbox.value.map(item => item.value));
    const missingWindMeter = expectedWindMeter.difference(new Set(windMeterItems.value));
    const labelsWindMeter = windMeterCheckbox.value.filter(item => missingWindMeter.has(item.value)).map(item => item.label);
    const passWindMeter = new Set(windMeterItems.value);
    const labelsWindMeterPass = windMeterCheckbox.value.filter(item => passWindMeter.has(item.value)).map(item => item.label);

    const expectedMast = new Set(mastCheckbox.value.map(item => item.value));
    const missingMast = expectedMast.difference(new Set(mastItems.value));
    const labelsMast = mastCheckbox.value.filter(item => missingMast.has(item.value)).map(item => item.label);
    const passMast = new Set(mastItems.value);
    const labelsMastPass = mastCheckbox.value.filter(item => passMast.has(item.value)).map(item => item.label);

    const totalExpected = expectedMast.size + expectedWindMeter.size + expectedRadar.size +
      expectedBoom.size + expectedWidescreenActuators.size + expectedLiDar.size +
      expectedWidescreenCamera.size + expectedLicensePlateCamera.size + expectedFaceCamera.size +
      expectedGeneral.size;
    const totalUnchecked = missingMast.size + missingWindMeter.size + missingRadar.size +
      missingBoom.size + missingWidescreenActuators.size + missingLiDar.size +
      missingWidescreenCamera.size + missingLicensePlateCamera.size + missingFaceCamera.size +
      missingGeneral.size;
    const totalChecked = totalExpected - totalUnchecked;

    reportStr =     reportStr + 'Total Tests:     ' + totalExpected + '\n';
    reportStr =     reportStr + 'Total Passed:    ' + totalChecked + '\n';
    reportStr =     reportStr + 'Total Failed:    ' + totalUnchecked + '\n';
    reportStr =     reportStr + 'Percent Passed:  ' + ((totalChecked / totalExpected) * 100.0) + '\n';
    reportStr =     reportStr + 'Percent Failed:  ' + ((totalUnchecked / totalExpected) * 100.0) + '\n';

    reportStr = reportStr + "\nFailed Tests\n";
    reportStr = reportStr + "=========================\n"

    if(labelsGeneral.length > 0){
      reportStr =  reportStr + 'General: ' + labelsGeneral.join(', ') + '\n';
      generateMaintTasks(labelsGeneral, 'BASE_UNIT', baseUnitName.value, 'General');
    }

    if(labelsBoom.length > 0){
      reportStr =  reportStr + 'Boom: ' + labelsBoom.join(', ') + '\n';
      generateMaintTasks(labelsBoom, 'BASE_UNIT', baseUnitName.value, 'Boom');
    }
    if(labelsRadar.length > 0){
      reportStr =  reportStr + 'Radar: ' + labelsRadar.join(', ') + '\n';
      generateMaintTasks(labelsRadar, 'BASE_UNIT', baseUnitName.value, 'Radar');
    }
    if(labelsMast.length > 0){
      reportStr =  reportStr + 'Mast: ' + labelsMast.join(', ') + '\n';
      generateMaintTasks(labelsMast, 'BASE_UNIT', baseUnitName.value, 'Mast');
    }
    if(labelsWindMeter.length > 0){
      reportStr =  reportStr + 'Wind Meter: ' + labelsWindMeter.join(', ') + '\n';
      generateMaintTasks(labelsWindMeter, 'BASE_UNIT', baseUnitName.value, 'Wind Meter');
    }

    if(missingFaceCamera.size > 0){
      for (const camera of faceCameras.value) {
        const missingFaceCameraList = [...missingFaceCamera];
        const missingForCamera = new Set(missingFaceCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = faceCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCamera) {
          activity_log('Camera', 
                       camera, 
                       "Face Camera Test: " + camera_item + " has failed",
                       technicianName.value);
        }
        console.log("Start => processing activity log for face cameras");
        const passForCamera = new Set(faceCameraItems.value.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        console.log("passForCamera=" + [...passForCamera]);
        const labelsForCameraPass = faceCameraCheckbox.value.filter(item => passForCamera.has(item.value)).map(item => item.label);
        console.log("labelsForCameraPass=" + labelsForCameraPass);
        for (const camera_item of labelsForCameraPass) {
          activity_log('Camera', 
                      camera, 
                      "Face Camera Test: " + camera_item + " has passed",
                      technicianName.value);
        }
        console.log("Done => processing activity log for face cameras");
        generateMaintTasks(labelsForCamera, 'CAMERA',camera, 'Face Camera');
        reportStr =  reportStr + 'Face Camera - ' + camera + ':' + labelsForCamera.join(', ') + '\n';
   
      }
    }

    if(missingLicensePlateCamera.size > 0){
      for (const camera of licensePlateCameras.value) {
        const missingLicensePlateCameraList = [...missingLicensePlateCamera];
        const missingForCamera = new Set(missingLicensePlateCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = licensePlateCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCamera) {
          activity_log('Camera', 
                      camera, 
                      "License Plate Camera Test: " + camera_item + " has failed",
                      technicianName.value);
        }
        const passForCamera = new Set(licensePlateCameraItems.value.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCameraPass = licensePlateCameraCheckbox.value.filter(item => passForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCameraPass) {
          activity_log('Camera', 
                      camera, 
                      "License Plate Camera Test: " + camera_item + " has passed",
                      technicianName.value);
        }
        generateMaintTasks(labelsForCamera, 'CAMERA',camera, 'License Plate Camera');
        reportStr =  reportStr + 'License Plate Camera - ' + camera + ':' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingWidescreenCamera.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingWidescreenCameraList = [...missingWidescreenCamera];
        const missingForCamera = new Set(missingWidescreenCameraList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = widescreenCameraCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCamera) {
          activity_log('Camera', 
                      camera, 
                      "Widescreen Camera Test: " + camera_item + " has failed",
                      technicianName.value);
        }
        const passForCamera = new Set(widescreenCameraItems.value.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCameraPass = widescreenCameraCheckbox.value.filter(item => passForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCameraPass) {
          activity_log('Camera', 
                      camera, 
                      "Widescreen Camera Test: " + camera_item + " has passed",
                      technicianName.value);
        }
        generateMaintTasks(labelsForCamera, 'CAMERA',camera, 'Widescreen Camera');
        reportStr =  reportStr + 'Widescreen Camera - ' + camera + ':' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingLiDar.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingLiDarList = [...missingLiDar];
        const missingForCamera = new Set(missingLiDarList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = liDarCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCamera) {
          activity_log('Camera', 
                      camera, 
                      "LiDar Test: " + camera_item + " has failed",
                      technicianName.value);
        }
        const passForCamera = new Set(liDarItems.value.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCameraPass = liDarCheckbox.value.filter(item => passForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCameraPass) {
          activity_log('Camera', 
                      camera, 
                      "LiDar Test: " + camera_item + " has passed",
                      technicianName.value);
        }
        generateMaintTasks(labelsForCamera, 'CAMERA',camera, 'LiDar');
        reportStr =  reportStr + 'LiDar - ' + camera + ':' + labelsForCamera.join(', ') + '\n';
      }
    }

    if(missingWidescreenActuators.size > 0){
      for (const camera of widescreenCameras.value) {
        const missingWidescreenActuatorsList = [...missingWidescreenActuators];
        const missingForCamera = new Set(missingWidescreenActuatorsList.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCamera = widescreenActuatorsCheckbox.value.filter(item => missingForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCamera) {
          activity_log('Camera', 
                      camera, 
                      "Widescreen Actuators Test: " + camera_item + " has failed",
                      technicianName.value);
        }
        const passForCamera = new Set(widescreenActuatorsItems.value.filter(item => item.includes('_' + camera)).map(item => item.replace('_' + camera, '')));
        const labelsForCameraPass = widescreenActuatorsCheckbox.value.filter(item => passForCamera.has(item.value)).map(item => item.label);
        for (const camera_item of labelsForCameraPass) {
          activity_log('Camera', 
                      camera, 
                      "Widescreen Actuators Test: " + camera_item + " has passed",
                      technicianName.value);
        }
        generateMaintTasks(labelsForCamera, 'CAMERA',camera, 'Widescreen Actuators');
        reportStr =  reportStr + 'Widescreen Actuators - ' + camera + ':' + labelsForCamera.join(', ') + '\n';
      }
    }
    for (const item of labelsGeneral) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "General Test: " + item + " has failed",
                     technicianName.value);
    }
    for (const item of labelsGeneralPass) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "General Test: " + item + " has passed",
                     technicianName.value);
    }
    for (const item of labelsBoom) {
      activity_log('Base Unit', 
                    props.base_unit, 
                    "Boom Test: " + item + " has failed",
                    technicianName.value);
    }
    for (const item of labelsBoomPass) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "Boom Test: " + item + " has passed",
                     technicianName.value);
    }
    for (const item of labelsRadar) {
      activity_log('Base Unit', 
                    props.base_unit, 
                    "Radar: " + item + " has failed",
                    technicianName.value);
    }
    for (const item of labelsRadarPass) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "Radar Test: " + item + " has passed",
                     technicianName.value);
    }
    for (const item of labelsWindMeter) {
      activity_log('Base Unit', 
                    props.base_unit, 
                    "Wind Meter: " + item + " has failed",
                    technicianName.value);
    }
    for (const item of labelsWindMeterPass) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "Wind Meter Test: " + item + " has passed",
                     technicianName.value);
    }
    for (const item of labelsMast) {
      activity_log('Base Unit', 
                    props.base_unit, 
                    "Mast: " + item + " has failed",
                    technicianName.value);
    }
    for (const item of labelsMastPass) {
        activity_log('Base Unit', 
                     props.base_unit, 
                     "Mast Test: " + item + " has passed",
                     technicianName.value);
    }
    console.log("OUT SystemTestChecklist.generateReport.");
    return reportStr;
  }

  // Go back to previous page
  const handleSubmit = async () => {
    console.log("IN SystemTestChecklist.handleSubmit. widescreenCameraItems=" + widescreenCameraItems.value);
    
    const dialogText = generateDialogText();
    const result = await confirmDialog.value.open(
      'Confirm Submit',
      dialogText,
      { color: 'red lighten-3' }
    );
    if (result) {
      const bu = await fetchBaseUnitByName();
      activity_log('Base Unit', 
                    props.base_unit, 
                    "System Test Checklist Executed",
                    technicianName.value);

      const description = generateReport(bu.location);
      await sendNote(bu.id, description);
      router.go(-2);
    } else {
      console.log("Submit cancelled");
    }
    console.log("OUT SystemTestChecklist.handleSubmit");
  };

  // This method handles the REST call to insert the note into the database.
  const sendNote = async (bu_id, description) => {
    console.log('IN SystemTestChecklist.sendNote');
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
        description: description,
        item_type: "BASE_UNIT",
        item_ref: bu_id
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/add-note', requestBody, config);
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
    console.log('OUT SystemTestChecklist.sendNote');
  };

  // This method handles the REST call to insert the maintenance task.
  const addMaintTask = async (description, itemType, itemName) => {
    console.log('IN SystemTestChecklist.addMaintTask');
    const config = {
      headers: {
          'Content-Type': 'application/json'
      }
    };
    const requestBody = {
      due_date: reportDate.value,
      description: description,
      item_type: itemType,
      item_name: itemName
    };
    console.log("requestBody=" + JSON.stringify(requestBody));
    try {
        const response = await api.post('/add-maintenance-task-by-name', requestBody, config);
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
    console.log('OUT SystemTestChecklist.addMaintTask');
  };

  const fetchBaseUnitByName = async () => {
    console.log("IN SystemTestChecklist.fetchBaseUnitByName");

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      name: baseUnitName.value
    };
    let target_bu = null;
    try {
        const response = await api.post('/get-base-unit-by-name', requestBody, config);
        target_bu = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching other-items:' + e,
            { color: 'red lighten-3' }
          );
    }
    console.log("OUT SystemTestChecklist.fetchBaseUnitByName");
    return target_bu;
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
    .checkbox-grid {
      display: grid;
      grid-template-columns: 1fr; /* Creates two equal-width columns */
      gap: 5px;
    }
  }
</style>
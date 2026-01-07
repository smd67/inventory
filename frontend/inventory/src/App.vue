<template>
  <v-app>
    <v-main>
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </v-main>

    <AppFooter />
  </v-app>
</template>

<script setup>
import Prototype from './components/Prototype.vue';

  //
</script>

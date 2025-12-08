<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
    <circle cx="12" cy="12" r="2" fill="currentColor"/>
    <!-- Сегменты колеса -->
    <path d="M12 2 L12 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M12 20 L12 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M2 12 L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M20 12 L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M5.05 5.05 L6.46 6.46" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M17.54 17.54 L18.95 18.95" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M5.05 18.95 L6.46 17.54" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M17.54 6.46 L18.95 5.05" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  </svg>
</template>

<script>
export default {
  name: 'WheelIcon',
  props: {
    size: {
      type: [Number, String],
      default: 24
    }
  }
}
</script>
<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="fixed z-50 inset-0 overflow-y-auto" @close="onClose">
      <div class="flex items-center justify-center min-h-screen px-4">
        <TransitionChild
          as="template"
          enter="ease-out duration-200" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100"
          leave="ease-in duration-150" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="bg-white dark:bg-gray-900 rounded-xl shadow-xl w-full max-w-md p-6">
            <DialogTitle class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ title }}</DialogTitle>
            <slot />
            <div class="flex justify-end gap-2 mt-6">
              <button @click="onClose" class="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600">Отмена</button>
              <button @click="onSave" class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Сохранить</button>
            </div>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue';
const props = defineProps({
  open: Boolean,
  title: String,
  onClose: Function,
  onSave: Function,
});
</script>

<style scoped>
</style>

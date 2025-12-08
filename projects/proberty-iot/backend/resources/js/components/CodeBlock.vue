<template>
  <div 
    class="code-block" 
    :class="{ 'code-block-numbered': showLineNumbers }"
  >
    <div 
      v-if="showLineNumbers" 
      class="line-numbers"
    >
      <div 
        v-for="lineNumber in totalLines" 
        :key="lineNumber"
      >
        {{ lineNumber }}
      </div>
    </div>
    <div class="code-content">
      <pre><code 
        ref="codeRef"
        :class="`language-${language}`"
      >{{ code }}</code></pre>
      <button 
        class="copy-code-btn" 
        @click="copyCode"
      >
        {{ copied ? 'Скопировано!' : 'Копировать' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-php'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'

const props = defineProps({
  code: {
    type: String,
    required: true
  },
  language: {
    type: String,
    default: 'javascript'
  },
  showLineNumbers: {
    type: Boolean,
    default: true
  }
})

const codeRef = ref(null)
const copied = ref(false)

const totalLines = computed(() => {
  return props.code.split('\n').length
})

const copyCode = () => {
  if (codeRef.value) {
    navigator.clipboard.writeText(props.code)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}

onMounted(() => {
  if (codeRef.value) {
    Prism.highlightElement(codeRef.value)
  }
})
</script>

<style scoped>
.copy-code-btn {
  z-index: 10;
}
</style>

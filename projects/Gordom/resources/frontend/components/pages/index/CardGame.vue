<template lang="pug">
    div(class="grid w-full grid-cols-4 2xl:grid-cols-3 xl:!grid-cols-2 xl:gap-4 sm:!gap-3 gap-6")
        router-link(v-for="item in games" :to="item.path ? item.path : '#'" :key="item.id" :class="item.path ? 'overflow-hidden rounded-2xl' : ''" class="grid w-full before:pt-[80%] relative")
            div(:class="item.name ? '' : 'hidden'" class="absolute left-0 top-[20px] bg-gradient-to-r from-[#1b1c20] min-w-[150px] to-transparent py-1 px-4 z-[1] font-['Rubik'] font-bold text-grayLight") {{ item.name }}
            div(class="absolute left-0 top-0 w-full h-full")
                img(:src="require('@/images/games/'+ item.image)" class="absolute left-0 top-0 w-full h-full" :class="item.path ? 'object-cover' : 'object-contain'")
            div(v-if="!item.path" class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 font-['Rubik'] font-bold text-gray text-6xl") ?
</template>

<script>
    export default {
        name: 'CardGame',
        props: {
            games: {
                type: Array,
                default: () => {}
            }
        }
    }
</script>

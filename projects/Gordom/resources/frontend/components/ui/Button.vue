<template lang="pug">
    div
        router-link(
            v-if="type === 'link'"
            :to="path"
            class="font-['Rubik'] whitespace-nowrap flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)]"
            :class="theme === null ? 'hover:bg-violetHover bg-violet' : '' || theme === 'gray' ? 'hover:bg-[#3A3A40] bg-[#2c2c31]' : '' || theme === 'red' ? 'hover:bg-redHover bg-red' : '' || theme === 'green' ? 'hover:bg-greenHover bg-green' : '' || classes"
        ) 
            svg(v-if="ico" class="w-[18px] h-[18px] text-current mr-2")
                use(:xlink:href="'images/symbols.svg#'+ico")
            | {{ text }}

        button(
            v-if="type === 'button'"
            type="submit"
            class="font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)]"
            :class="theme === null ? 'hover:bg-violetHover bg-violet' : '' || theme === 'gray' ? 'hover:bg-[#3A3A40] bg-[#2c2c31]' : '' || theme === 'red' ? 'hover:bg-redHover bg-red' : '' || theme === 'green' ? 'hover:bg-greenHover bg-green' : '' || classes"
        ) 
            svg(v-if="ico" class="w-[18px] h-[18px] text-current mr-2")
                    use(:xlink:href="'images/symbols.svg#'+ico")
            | {{ text }}

</template>

<script>
    export default {
        props: {
            text: {
                type: String,
                default: () => {}
            },
            theme: {
                type: String,
                default: () => {}
            },
            type: {
                type: String,
                default: () => {}
            },
            ico: {
                type: String,
                default: () => {}
            },
            path: {
                type: String,
                default: () => {}
            },
            classes: {
                type: String,
                default: () => {}  
            },
        }
    }
</script>

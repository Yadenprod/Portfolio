<template lang="pug">
  div(class="w-full overflow-hidden rounded-xl cursor-pointer transition-transform hover:-translate-y-2" @click="$router.push('/slots/' + data.game_id)")
    div(class="bg-gray")
      img(:src="data.icon" class="w-full h-[200px] object-cover object-center")

    div(class="flex flex-col gap-2 px-4 py-4 bg-[#3A3A43]")
      h3(class="text-white font-bold leading-none select-none pointer-events-none text-ellipsis overflow-hidden whitespace-nowrap ") {{ data.title }}
      p(class="text-gray text-sm leading-none select-none pointer-events-none") {{ data.provider }}
</template>

<script>
export default {
    props: ['data'],
	name: 'SlotCard',
}
</script>

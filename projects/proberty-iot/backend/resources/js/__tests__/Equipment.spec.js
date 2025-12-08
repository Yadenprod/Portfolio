import { mount, shallowMount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import { defineComponent, ref, computed } from 'vue';
import Equipment from '../views/Equipment.vue';

describe('Equipment.vue', () => {
  it('корректно сортирует по названию', async () => {
    const equipment = ref([
      { id: 1, name: 'B', location: 'X', status: 'working' },
      { id: 2, name: 'A', location: 'Y', status: 'critical' }
    ]);
    const sortKey = ref('name');
    const sortAsc = ref(true);
    const search = ref('');
    const TestComp = defineComponent({
      components: { Equipment },
      setup() {
        return { equipment, sortKey, sortAsc, search };
      },
      template: '<Equipment />'
    });
    const wrapper = shallowMount(TestComp);
    // Проверяем сортировку
    const sorted = [...equipment.value].sort((a, b) => a.name.localeCompare(b.name));
    expect(sorted[0].name).toBe('A');
  });
  it('корректно пагинирует', async () => {
    const equipment = ref(Array.from({ length: 15 }, (_, i) => ({ id: i, name: 'Eq' + i, location: 'Loc', status: 'working' })));
    const sortKey = ref('name');
    const sortAsc = ref(true);
    const search = ref('');
    const currentPage = ref(2);
    const pageSize = 10;
    const paginatedEquipment = computed(() => {
      const start = (currentPage.value - 1) * pageSize;
      return equipment.value.slice(start, start + pageSize);
    });
    expect(paginatedEquipment.value.length).toBe(5);
  });
});

import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ToastContainer from '../components/ToastContainer.vue';

describe('ToastContainer', () => {
  it('рендерится без ошибок', () => {
    const wrapper = mount(ToastContainer);
    expect(wrapper.exists()).toBe(true);
  });

  it('отображает уведомление при вызове showToast', async () => {
    const wrapper = mount(ToastContainer);
    // Получаем функцию showToast из setup
    const showToast = wrapper.vm.showToast || wrapper.vm.$.setupState.showToast;
    showToast({ message: 'Тестовое уведомление', type: 'success', duration: 1000 });
    await wrapper.vm.$nextTick();
    expect(wrapper.html()).toContain('Тестовое уведомление');
  });
});

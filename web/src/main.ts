import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { directive } from '/@/utils/directive';
import { i18n } from '/@/i18n/index';
import other from '/@/utils/other';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';
import mitt from 'mitt';
import VueGridLayout from 'vue-grid-layout';
import piniaPersist from 'pinia-plugin-persist'
// @ts-ignore
import fastCrud from './settings.ts'
import pinia from './stores';

const app = createApp(App);
pinia.use(piniaPersist)

directive(app);
other.elSvg(app);

app.use(pinia).use(router).use(ElementPlus, { i18n: i18n.global.t }).use(i18n).use(VueGridLayout).use(fastCrud).mount('#app');

app.config.globalProperties.mittBus = mitt();

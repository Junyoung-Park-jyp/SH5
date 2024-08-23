import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import DateFnsAdapter from '@date-io/date-fns';
import ko from 'date-fns/locale/ko';  // 한국어 로케일 가져오기
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  date: {
    adapter: DateFnsAdapter,
    locale: {
      defaultLocale: 'ko',  // 기본 로케일을 한국어로 설정
      ko,  // 'ko' 키에 한국어 로케일 객체 할당
    },
  },
})
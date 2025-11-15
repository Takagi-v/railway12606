<template>
  <div class="service-lg">
    <div class="service-lg-wrapper">
      <div class="service-lg-grid" id="g-service-lg-grid">
        <a v-for="item in items" :key="item.href" :href="item.href" target="_blank" :title="item.title">
          <img :src="item.src" :alt="item.title" @error="onImgError($event, item.remoteSrc)" />
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 复刻官网 service-lg 四张大图，默认引用本地副本，加载失败自动回退到官网地址
const items = ref([
  {
    href: 'https://cx.12306.cn/tlcx/index.html',
    title: '铁路畅行 惠享出行 尊享体验',
    localSrc: '/assets/12306/images/abanner01.jpg',
    remoteSrc: 'https://www.12306.cn/index/images/abanner01.jpg'
  },
  {
    href: 'https://exservice.12306.cn/excater/index.html',
    title: '餐饮·特产 带有温度的旅行配餐',
    localSrc: '/assets/12306/images/abanner02.jpg',
    remoteSrc: 'https://www.12306.cn/index/images/abanner02.jpg'
  },
  {
    href: 'https://kyfw.12306.cn/otn/view/my_insurance.html',
    title: '铁路保险 用心呵护 放心出行',
    localSrc: '/assets/12306/images/abanner05.jpg',
    remoteSrc: 'https://www.12306.cn/index/images/abanner05.jpg'
  },
  {
    href: 'https://kyfw.12306.cn/otn/view/commutation_index.html',
    title: '计次订票开售 直刷乘车、出行乐无忧',
    localSrc: '/assets/12306/images/abanner06.jpg',
    remoteSrc: 'https://www.12306.cn/index/images/abanner06.jpg'
  }
].map(i => ({ ...i, src: i.localSrc })))

const onImgError = (e, remote) => {
  const img = e.target
  // 避免无限循环，仅在当前 src 不是远程地址时回退
  if (img && img.src !== remote) {
    img.src = remote
  }
}
</script>

<style scoped>
.service-lg { margin-top: 20px; }
/* 设定容器宽度并居中，避免与官网 .wrapper 冲突 */
.service-lg-wrapper { width: 1190px; max-width: 1190px; margin: 0 auto; padding: 0; }

/* 独立网格容器，避免被官网 .service-lg ul/li 规则干扰 */
.service-lg-grid {
  width: 1190px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 590px);
  column-gap: 10px;
  row-gap: 20px;
}

.service-lg-grid a { display: block; width: 590px; height: 160px; }
.service-lg-grid img {
  display: block;
  width: 590px;
  height: 160px;
  object-fit: cover;
}
</style>
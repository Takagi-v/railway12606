<template>
  <div class="section-service">
    <ul class="service-list">
      <li style="display: none">
        <a href="javascript:;" @click.prevent="goPickup">
          <i class="service-icon ico-s1"></i>
          <div>接送站</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goSpecialPassenger">
          <i class="service-icon ico-s2"></i>
          <div>重点旅客预约</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goLostItems">
          <i class="service-icon ico-s6"></i>
          <div>遗失物品查找</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goCarBooking">
          <i class="service-icon ico-s4"></i>
          <div>约车服务</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goShipping">
          <i class="service-icon ico-s5"></i>
          <div>便民托运</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goStationGuide">
          <i class="service-icon ico-s3"></i>
          <div>车站引导</div>
        </a>
      </li>
      <li>
        <a href="javascript:;" @click.prevent="goServiceShowcase">
          <i class="service-icon ico-s7"></i>
          <div>站车风采</div>
        </a>
      </li>
      <li class="last">
        <a href="javascript:;" @click.prevent="goFeedback">
          <i class="service-icon ico-s9"></i>
          <div>用户反馈</div>
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 与首页路由保持一致的跳转
const goPickup = () => {
  // 站接送当前官网项隐藏，这里先指向约车服务以保持体验连贯
  router.push({ name: 'car-booking' })
}
const goSpecialPassenger = () => router.push({ name: 'special-passenger' })
const goLostItems = () => router.push({ name: 'lost-items' })
const goCarBooking = () => router.push({ name: 'car-booking' })
const goShipping = () => router.push({ name: 'shipping' })
const goStationGuide = () => router.push({ name: 'station-guide' })
const goServiceShowcase = () => router.push({ name: 'service-showcase' })
const goFeedback = () => router.push({ name: 'user-feedback' })
</script>

<style scoped>
/* 复刻官网 service-list 样式 */
.service-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.service-list:before,
.service-list:after {
  content: '';
  display: table;
}
.service-list:after {
  clear: both;
  overflow: hidden;
}

.service-list li {
  float: left;
  width: 14.2%;
  height: 136px;
  padding: 35px 0;
  line-height: 20px;
  text-align: center;
  background-image: url('/assets/12306/images/line01.png');
  background-image: -webkit-image-set(
    url('/assets/12306/images/line01.png') 1x,
    url('/assets/12306/images/line01@2x.png') 2x
  );
  background-image: image-set(
    url('/assets/12306/images/line01.png') 1x,
    url('/assets/12306/images/line01@2x.png') 2x
  );
  background-position: right center;
  background-repeat: no-repeat;
}
.service-list li a {
  display: block;
  height: 66px;
  transition: 0.3s linear color;
  color: #333;
}
.service-list li:hover .service-icon {
  opacity: 0.8;
}
.service-list .last {
  background: none;
}

.service-list .service-icon {
  display: block;
  width: 36px;
  height: 36px;
  margin: 0 auto 5px;
  transition: 0.3s linear opacity;
  background-image: url('/assets/12306/images/service.png');
  background-image: -webkit-image-set(
    url('/assets/12306/images/service.png') 1x,
    url('/assets/12306/images/service@2x.png') 2x
  );
  background-image: image-set(
    url('/assets/12306/images/service.png') 1x,
    url('/assets/12306/images/service@2x.png') 2x
  );
}

/* 精确定位雪碧图各图标位置 */
.service-list .ico-s1 {
  background-position: 0 0;
}
.service-list .ico-s2 {
  background-position: 0 -40px;
}
.service-list .ico-s3 {
  background-position: 0 -80px;
}
.service-list .ico-s4 {
  background-position: 0 -120px;
}
.service-list .ico-s5 {
  background-position: 0 -160px;
}
.service-list .ico-s6 {
  background-position: 0 -200px;
}
.service-list .ico-s7 {
  background-position: 0 -240px;
}
.service-list .ico-s8 {
  background-position: 0 -280px;
}
.service-list .ico-s9 {
  background-position: 0 -320px;
}
.service-list .ico-s10 {
  background-position: 0 -360px;
}

/* 区块容器（与首页节距保持协调） */
.section-service {
  margin-top: 20px;
}
</style>

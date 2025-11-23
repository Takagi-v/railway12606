<template>
  <footer class="login-footer">
    <div class="footer-content">
      <div class="footer-columns">
        <section class="partner-links">
          <h4>友情链接</h4>
          <div class="partner-grid">
            <img :src="link02" alt="中国国家铁路集团有限公司" class="partner-image" />
            <img :src="link03" alt="中国铁路投资有限公司" class="partner-image" />
            <img :src="link04" alt="中国铁路95306网" class="partner-image" />
            <img :src="link05" alt="CRE中国铁路装备" class="partner-image" />
          </div>
        </section>

        <section class="qr-block">
          <h4>中国铁路官方微信</h4>
          <img :src="imgWeChat" alt="中国铁路官方微信" class="qr-img" />
        </section>

        <section class="qr-block">
          <h4>中国铁路官方微博</h4>
          <img :src="imgWeibo" alt="中国铁路官方微博" class="qr-img" />
        </section>

        <section class="qr-block">
          <h4>12306 公众号</h4>
          <img :src="imgPublic" alt="12306 公众号" class="qr-img" />
        </section>

        <section class="app-download">
          <h4>铁路12306</h4>
          <img :src="imgDownload" alt="铁路12306 官方APP下载" class="download-image" />
        </section>

        <section class="app-note">
          <p>官方APP下载，目前铁路未授权其他网站或APP开展类似服务内容，敬请广大用户注意。</p>
        </section>
      </div>
    </div>
    
    <div class="footer-txt">
      <div class="footer-txt-inner">
        <p class="footer-line">版权所有©2008-2025 中国铁道科学研究院集团有限公司 技术支持：铁旅科技有限公司</p>
        <p class="footer-line"><img :src="imgGongan" alt="公安备案" class="footer-icon" />京公网安备 11010802038392号  |  京ICP备05020493号-4  |  ICP证：京B2-20202537</p>
        <div class="footer-right"><img :src="imgFooterSlh" alt="适老化 无障碍服务" class="footer-slh" /></div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const link02 = new URL('../../pics/link02.png', import.meta.url).href
const link03 = new URL('../../pics/link03.png', import.meta.url).href
const link04 = new URL('../../pics/link04.png', import.meta.url).href
const link05 = new URL('../../pics/link05.png', import.meta.url).href
const imgWeChat = new URL('../../pics/zgtlwx.png', import.meta.url).href
const imgWeibo = new URL('../../pics/zgtlwb.png', import.meta.url).href
const imgPublic = new URL('../../pics/public.png', import.meta.url).href
const imgDownload = new URL('../../pics/download.png', import.meta.url).href
const imgGongan = new URL('../../pics/gongan.png', import.meta.url).href
const imgFooterSlh = new URL('../../pics/footer-slh.jpg', import.meta.url).href
</script>

<style scoped>
.login-footer {
  background: #f5f5f5;
  padding: 30px 0 0;
  border-top: 1px solid #e8e8e8;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-columns {
  display: grid;
  grid-template-columns: 420px 140px 140px 140px 140px 220px;
  gap: 0;
  align-items: start;
}

.footer-columns .partner-links {
  margin-bottom: 0;
}

.partner-grid {
  display: grid;
  grid-template-columns: repeat(2, 200px);
  gap: 16px;
  justify-items: start;
  align-items: center;
}

.partner-image {
  width: 200px;
  height: 34px;
  object-fit: contain;
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 0;
  box-sizing: border-box;
}

.qr-block h4 {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.qr-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qr-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  display: block;
}

.app-download h4 {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.app-download {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.download-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  display: block;
}

.app-note {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  padding: 4px;
  margin-top: 8px;
  align-self: center;
}

/* 底部版权文本 */
.footer-txt {
  background: #666666;
  color: #c1c1c1;
  height: 80px;
  display: flex;
  align-items: center;
}

.footer-txt-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  text-align: center;
  position: relative;
  padding-right: 170px;
}

.footer-line {
  margin: 0;
}

.footer-icon {
  width: 16px;
  height: 16px;
  margin-right: 6px;
  vertical-align: middle;
}

.footer-right {
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
}

.footer-slh {
  display: block;
}
</style>
<template>
  <div class="news-tab">
    <div class="tab-hd">
      <ul class="lists">
        <li :class="{ active: activeTab === 'latest' }" @click="activeTab = 'latest'">
          <a id="index_ads" name="index_ads" href="javascript:void(0)">最新发布</a>
        </li>
        <li :class="{ active: activeTab === 'faq' }" @click="activeTab = 'faq'">
          <a href="javascript:void(0)">常见问题</a>
        </li>
        <li :class="{ active: activeTab === 'credit' }" @click="activeTab = 'credit'">
          <a href="javascript:void(0)">信用信息</a>
        </li>
      </ul>
    </div>

    <div class="tab-bd">
      <div class="news-index">
        <!-- 最新发布（左右两列） -->
        <div class="news-index-columns" v-show="activeTab === 'latest'">
          <ul class="news-index-list state col">
            <li v-for="item in latestLeft" :key="item.href">
              <a
                target="_self"
                class="news-tit"
                :title="item.title"
                :href="item.href"
              >{{ item.title }}</a>
              <em class="news-time">{{ item.time }}</em>
            </li>
          </ul>
          <ul class="news-index-list state col">
            <li v-for="item in latestRight" :key="item.href">
              <a
                target="_self"
                class="news-tit"
                :title="item.title"
                :href="item.href"
              >{{ item.title }}</a>
              <em class="news-time">{{ item.time }}</em>
            </li>
          </ul>
        </div>

        <!-- 常见问题（左右两列） -->
        <div class="news-index-columns" v-show="activeTab === 'faq'">
          <ul class="news-index-list question col">
            <li v-for="item in faqLeft" :key="item.title">
              <a
                name="g_href"
                data-type="2"
                :data-href="item.dataHref"
                data-redirect="Y"
                data-target="_blank"
                href="javascript:;"
                class="news-tit"
              >{{ item.title }}</a>
            </li>
          </ul>
          <ul class="news-index-list question col">
            <li v-for="item in faqRight" :key="item.title">
              <a
                name="g_href"
                data-type="2"
                :data-href="item.dataHref"
                data-redirect="Y"
                data-target="_blank"
                href="javascript:;"
                class="news-tit"
              >{{ item.title }}</a>
            </li>
          </ul>
        </div>

        <!-- 信用信息：按官网结构复现为两列面板 -->
        <div class="credit-panel" v-show="activeTab === 'credit'">
          <div class="discredit-list-box">
            <!-- 失信被执行人(自然人)公示 -->
            <dl class="discredit-list">
              <dt>
                <span class="icon-wrap" aria-hidden="true">
                  <svg class="icon-svg" viewBox="0 0 1024 1024" focusable="false" role="img" aria-hidden="true">
                    <g transform="matrix(1 0 0 -1 0 1024)">
                      <path d="M827.74360039 34.55275752a10.90863721 10.90863721 0 0 0-7.432258 10.42913672v16.90239287a28.94984385 28.94984385 0 0 1-28.94984385 28.94984385H217.27950049c-15.98834531 0-28.94984385-12.96149854-28.94984385-28.94984385v-12.52695058a10.96857422 10.96857422 0 0 0-9.29032295-10.84869932C127.97814746 30.535067870000034 90.33267412-13.44318426999996 90.33173809-65.12341317999994h809.69656553c-0.02622305 45.35400586-29.18397481 85.55993789-72.28470323 99.6761707z m88.94734628 161.53173808L609.93048886 481.80686807l110.28512022 110.22518144c10.21373526-10.18751308 26.64786709-10.18751308 36.80166446-0.05993701 11.21394375 11.19240352 11.21394375 27.64620175 1.07887587 37.82060332L561.50093692 826.3879292c-10.17346553 10.13506787-26.62819981 10.13506787-36.80166534 0-5.97596221-5.89073906-8.72934434-12.51196699-8.72934434-19.4197711 0-6.90780411 2.75338213-13.52996895 7.65046846-18.40083222L248.98647237 513.87346553c-10.23340253 10.19500489-26.6881377 10.19500489-36.86160235 0.05993701-11.09406885-11.19240352-11.09406885-27.64620175-0.95900098-37.82060332l196.59521338-196.65515127c10.17346553-10.13506787 26.62819981-10.13506787 36.80166446 0 11.14651406 11.23267412 11.14651406 27.66680508 1.01893887 37.8206042L555.74693018 427.62330937 841.46930263 120.86285155999997a53.16461982 53.16461982 0 0 1 76.6002085-1.31862656 53.16461982 53.16461982 0 0 1-1.37856445 76.5402706zM325.88636856 490.91737734c-4.20967705-4.19094668-11.01446367-4.19094668-15.22414161 0l-0.47950049 0.47950049c-4.19094668 4.20967705-4.19094668 11.01446367 0 15.2241416l220.75005147 220.75005235c4.19562949 4.19562949 11.08844912 4.19562949 15.28407949 0l0.35962558-0.4195626c4.19094668-4.20967705 4.19094668-11.01446367 0-15.2241416L325.88636856 490.91737734z"></path>
                    </g>
                  </svg>
                </span>
                失信被执行人(自然人)公示
              </dt>
              <div class="discredit-demo">
                <div class="discredit-empty">
                  <img
                    src="https://www.12306.cn/index/images/empty.png"
                    alt="暂无公示数据"
                  />
                  <div class="empty-text">暂无公示数据</div>
                </div>
              </div>
              <dd class="more">
                <a
                  name="g_href"
                  data-type="6"
                  data-href="queryDishonest/init"
                  data-redirect="Y"
                  data-target="_blank"
                  href="javascript:;"
                >更多&gt;</a>
              </dd>
            </dl>

            <!-- 失信已执行人(自然人)公布 -->
            <dl class="discredit-list">
              <dt>
                <span class="icon-wrap" aria-hidden="true">
                  <svg class="icon-svg" viewBox="0 0 1024 1024" focusable="false" role="img" aria-hidden="true">
                    <g transform="matrix(1 0 0 -1 0 1024)">
                      <path d="M986.609375-11.5078125H116.4921875v19.722656C116.4921875 26.4609375 136.79492213 41.22656274999997 161.84374975 41.22656274999997h779.414063c25.04882838 0 45.35156225-14.76562525 45.35156225-33.01171925V-11.5078125zM923.06445338 102.76757838000003h-0.13183619V454.32128906h0.10546849c20.56640625 0 37.20410131 15.74121094 37.20410207 35.14746069h-148.76367212c0-19.40624975 16.63769506-35.14746068 37.17773437-35.14746069h0.1054685v-351.55371068h-0.1054685c-20.54003932 0-37.17773438-15.74121094-37.17773437-35.14746145H960.24218775c0 19.40624975-16.66406275 35.14746068-37.17773437 35.14746145zM142.85937475 489.41601588c0-19.40624975 16.66406275-35.12109375 37.17773437-35.12109375h0.13183619v-351.52734375H180.03710912C159.47070287 102.76757838000003 142.85937475 87.02636743999994 142.85937475 67.59375h148.76367213c0 19.40624975-16.63769506 35.14746068-37.17773438 35.14746068h-0.1054685V454.32128906h0.1054685c20.54003932 0 37.17773438 15.74121094 37.17773438 35.14746069H142.85937475v-0.05273387z m335.179688-35.06835988c20.56640625 0 37.17773438 15.714844 37.17773438 35.12109375H366.453125c0-19.40624975 16.66406275-35.14746068 37.17773438-35.14746069h0.13183619v-351.55371068h-0.10546926c-20.56640625 0-37.17773438-15.74121094-37.17773438-35.14746145h148.76367213c0 19.40624975-16.66406275 35.14746068-37.17773437 35.14746145h-0.13183619V454.32128906h0.10546925z m111.21679688 35.06835988c0-19.40624975 16.66406275-35.12109375 37.17773437-35.12109375h0.13183543v-351.55371145h-0.10546849c-20.56640625 0-37.17773438-15.74121094-37.17773438-35.14746068h148.76367213c0 19.40624975-16.66406275 35.14746068-37.20410207 35.14746068h-0.10546849V454.32128906h0.10546849c20.54003932 0 37.17773438 15.74121094 37.17773438 35.14746069H589.25585963v-0.05273387zM961.50781275 594.5947263099999L571.80078125 775.078125a48.43652318 48.43652318 0 0 1-40.47363307 0L141.59374975 594.5947263099999C126.22167969 587.47558568 116.4921875 572.92089818 116.4921875 556.9687502500001v-20.09179687c0-11.60156275 10.15136693-21.04101563 22.6757815-21.04101563h824.7656245c12.52441381 0 22.6757815 9.41308594 22.6757815 21.04101563V556.9687502500001c0 15.95214869-9.72949219 30.53320313-25.10156225 37.62597606zM552.6054685 574.3710940000001c-39.99902369 0-72.40429662 30.11132838-72.40429663 67.23632813s32.43164063 67.23632813 72.40429663 67.23632812 72.40429662-30.11132838 72.40429738-67.23632812a64.86328125 64.86328125 0 0 0-21.22558645-47.54003906 75.33105443 75.33105443 0 0 0-51.17871093-19.69628907z"></path>
                    </g>
                  </svg>
                </span>
                失信已执行人(自然人)公布
              </dt>
              <div class="discredit-demo">
                <div class="discredit-empty">
                  <img
                    src="https://www.12306.cn/index/images/empty.png"
                    alt="暂无公示数据"
                  />
                  <div class="empty-text">暂无公示数据</div>
                </div>
              </div>
              <dd class="more">
                <a
                  name="g_href"
                  data-type="6"
                  data-href="queryDishonest/init"
                  data-redirect="Y"
                  data-target="_blank"
                  href="javascript:;"
                >更多&gt;</a>
              </dd>
            </dl>
          </div>
        </div>

        <div class="news-more">
          <a
            name="g_href"
            data-type="4"
            data-href="zxdt/index_zxdt.html"
            data-redirect="Y"
            href="javascript:;"
            data-target="_blank"
          >更多&gt;</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('latest')

const latestList = ref([
  { title: '公 告', href: 'http://www.12306.cn/mormhweb/zxdt/202412/t20241211_43192.html', time: '2024-12-11' },
  { title: '关于铁路客运推广使用全面数字化的电子发票的公告', href: 'http://www.12306.cn/mormhweb/zxdt/202410/t20241023_43048.html', time: '2024-11-07' },
  { title: '关于优化铁路车票改签规则的公告', href: 'http://www.12306.cn/mormhweb/zxdt/202401/t20240111_40579.html', time: '2024-01-11' },
  { title: '外国护照身份核验使用说明', href: 'http://www.12306.cn/mormhweb/zxdt/202311/t20231127_40375.html', time: '2023-12-13' },
  { title: '铁路旅客禁止、限制携带和托运物品目录', href: 'http://www.12306.cn/mormhweb/zxdt/202206/t20220617_37625.html', time: '2023-11-30' },
  { title: '候补购票操作说明', href: 'http://www.12306.cn/mormhweb/zxdt/201905/t20190521_22980.html', time: '2024-04-19' },
  { title: '公 告', href: 'http://www.12306.cn/mormhweb/zxdt/201512/t20151201_3949.html', time: '2022-12-22' },
  { title: '关于铁路车站起售时间的公告', href: 'http://www.12306.cn/mormhweb/zxdt/201411/t20141126_2316.html', time: '2025-11-14' },
  { title: '中国铁路成都局集团有限公司关于2025年11月15日至26日加开部分列车的公告', href: 'http://www.12306.cn/mormhweb/zxdt_news/202511/t20251114_45061.html', time: '2025-11-14' },
  { title: '中国铁路成都局集团有限公司关于2025年11月14日至26日加开部分列车的公告', href: 'http://www.12306.cn/mormhweb/zxdt_news/202511/t20251113_45058.html', time: '2025-11-13' },
])

const faqList = ref([
  { title: '实名制车票', dataHref: 'gonggao/realNameTicket.html' },
  { title: '售票窗口购票', dataHref: 'gonggao/ticketWindow.html' },
  { title: '互联网购票', dataHref: 'gonggao/onlineBooking.html' },
  { title: '互联网退票', dataHref: 'gonggao/onlineRefund.html' },
  { title: '随身携带品', dataHref: 'gonggao/carryGoods.html' },
  { title: '进出站', dataHref: 'gonggao/enterExit.html' },
  { title: '丢失购票时使用的有效身份证件', dataHref: 'gonggao/lostIdCard.html' },
  { title: '使用居民身份证直接检票乘车', dataHref: 'gonggao/idCardDirectCheck.html' },
  { title: '广深港跨境列车', dataHref: 'gonggao/hsrCrossBorder.html' },
])

const creditList = ref([])

// 左右两列分配（参考官网：列表一分为二列）
const latestLeft = computed(() => latestList.value.slice(0, Math.ceil(latestList.value.length / 2)))
const latestRight = computed(() => latestList.value.slice(Math.ceil(latestList.value.length / 2)))
const faqLeft = computed(() => faqList.value.slice(0, Math.ceil(faqList.value.length / 2)))
const faqRight = computed(() => faqList.value.slice(Math.ceil(faqList.value.length / 2)))
</script>

<style scoped>
.news-tab {
  max-width: 1190px;
  margin: 20px auto; /* 与上方 servicelg 留出空隙 */
  background: #fff;
}

.tab-hd {
  border: 1px solid #e5e5e5;
  border-radius: 4px 4px 0 0;
  background: #f4f5f7;
}

.lists {
  display: flex;
  flex-wrap: nowrap;
  align-items: stretch;
  margin: 0;
  padding: 0;
  list-style: none;
}

.lists li {
  flex: 0 0 180px;
}

.lists li a {
  display: flex;               /* 让文字在单元格内水平、垂直居中 */
  align-items: center;
  justify-content: center;
  height: 42px;                /* 固定高度以保证居中感知一致 */
  padding: 0;
  color: #333;
  text-decoration: none;
}

.lists li.active a {
  background: #2e64fe;
  color: #fff;
  border-radius: 4px 4px 0 0;
}

.tab-bd {
  border: 1px solid #e5e5e5;
  border-top: none;
  border-radius: 0 0 4px 4px;
}

.news-index {
  width: 1148px;
  margin: 0 auto;
  padding: 12px 16px 10px;     /* 左右增加内边距，避免内容贴边 */
}

/* 左右两列容器（参考官网两列布局） */
.news-index-columns {
  display: flex;
  gap: 24px;                  /* 两列间距，避免右侧溢出 */
}
.news-index-list.col {
  flex: 1 1 0;                /* 两列等宽 */
}

.news-index-list {
  margin: 0;                   /* 移除负边距，防止内容过于靠近右边栏 */
  padding: 0;
  list-style: none;
}

.news-index-list li {
  position: relative;            /* 蓝点绝对定位的参考 */
  height: 36px;
  line-height: 36px;             /* 与官网一致的行高 */
  box-sizing: border-box;
}

/* 按有/无日期分别采用网格布局，保证列宽与对齐精确 */
.news-index-list.state li {
  display: grid;
  grid-template-columns: 16px minmax(0, 1fr) 100px; /* 左侧缩进、标题、日期固定宽度，标题允许收缩 */
  align-items: center;
  column-gap: 12px;
  padding: 0 12px;               /* 左右留白，防止被边界遮挡 */
}
.news-index-list.question li {
  display: grid;
  grid-template-columns: 16px minmax(0, 1fr);       /* 无日期两列，标题允许收缩 */
  align-items: center;
  column-gap: 12px;
  padding: 0 12px;               /* 左右留白 */
}

.news-index-list li::before {
  content: '';
  position: absolute;
  left: 8px;                   /* 与网格的 16px 缩进对齐 */
  top: 50% !important;         /* 强制使用 top 居中，避免被 bottom 规则覆盖 */
  bottom: auto !important;
  transform: translateY(-50%) !important; /* 垂直居中，与文本对齐 */
  width: 6px;
  height: 6px;
  background: #3b99fc;
}

.news-tit {
  /* 在网格布局中占据 1fr 列，允许收缩以显示省略号 */
  min-width: 0;                 /* 允许收缩，配合省略号避免挤压日期 */
  color: #333;
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
  margin: 0;                    /* 网格列间距由 column-gap 控制 */
  line-height: 36px;            /* 与 li 保持一致，蓝点居中更准 */
}
/* 明确指定标题与日期在网格中的列位置，避免标题落在缩进列导致变窄 */
.news-index-list.state .news-tit { grid-column: 2; }
.news-index-list.state .news-time { grid-column: 3; }
.news-index-list.question .news-tit { grid-column: 2; }

.news-tit:hover { color: #2e64fe; }

.news-time {
  color: #999;
  font-size: 12px;
  width: 100px;
  text-align: right;
  line-height: 36px;            /* 与 li 保持一致，提升垂直对齐 */
  justify-self: end;            /* 在网格中右对齐且固定宽度不被挤压 */
}

/* 常见问题无日期列：标题占满剩余空间 */
.news-index-list.question .news-tit {
  max-width: 100%;
  margin-right: 0;
  line-height: 36px;            /* 保证与蓝点对齐 */
}

/* 信用信息无日期列：标题占满剩余空间 */
.news-index-list.credit .news-tit {
  max-width: 100%;
  margin-right: 0;
}

.news-more { text-align: right; padding-top: 8px; }
.news-more a { color: #2e64fe; text-decoration: none; }

/* 信用信息面板（复刻官网双列结构） */
.credit-panel { padding: 4px 0 10px; }
.discredit-list-box {
  display: flex;
  gap: 24px;
}
.discredit-list {
  flex: 1 1 0;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
}
.discredit-list dt {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #333;
  background: #f7f8fa;
  border-bottom: 1px solid #eee;
}
.discredit-list dt .icon-wrap { display: inline-flex; align-items: center; justify-content: center; }
.discredit-list dt .icon-svg { width: 18px; height: 18px; fill: #2e64fe; display: inline-block; }
.discredit-demo {
  height: 128px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.discredit-empty { text-align: center; }
.discredit-empty img {
  display: block;
  width: 100px;
  height: 80px;
  margin: 15px auto;
}
.discredit-empty .empty-text { color: #999; }
.discredit-list .more { text-align: right; padding: 8px 12px; }
.discredit-list .more a { color: #2e64fe; text-decoration: none; }
</style>
<template>
  <div
    class="city-selector"
    v-show="visible"
    :style="{ top: top + 'px', left: left + 'px' }"
    @mousedown.prevent
  >
    <!-- Left Sidebar -->
    <div class="city-selector-sidebar">
      <div class="sidebar-item active">国内站点</div>
      <div class="sidebar-item">国际站点</div>
    </div>

    <!-- Right Content Area -->
    <div class="city-selector-main">
      <!-- Header -->
      <div class="city-selector-header">
        拼音支持首字母输入
      </div>

      <!-- Tabs -->
      <div class="city-selector-tabs">
        <div
          v-for="tab in tabs"
          :key="tab.key"
          class="city-selector-tab"
          :class="{ active: currentTab === tab.key }"
          @click="currentTab = tab.key"
        >
          {{ tab.label }}
        </div>
      </div>

      <!-- City List Content -->
      <div class="city-selector-content">
        <div v-if="currentTab === 'hot'" class="city-list hot-list">
          <div
            v-for="city in hotCities"
            :key="city.code"
            class="city-item"
            @click="selectCity(city)"
          >
            {{ city.name }}
          </div>
        </div>
        <div v-else class="city-list-group-container">
          <div v-for="(cities, letter) in currentCitiesGroup" :key="letter" class="city-group-row">
            <div class="city-group-letter">{{ letter }}</div>
            <div class="city-group-list">
              <div
                v-for="city in cities"
                :key="city.code"
                class="city-item"
                @click="selectCity(city)"
              >
                {{ city.name }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer / Pagination -->
      <div class="city-selector-footer" v-if="currentTab !== 'hot' && totalPages > 1">
        <div class="pagination-controls">
          <span
            class="page-btn"
            :class="{ disabled: currentPage === 1 }"
            @click="currentPage > 1 && (currentPage--)"
          >
            &laquo; 上一页
          </span>
          <span class="page-info"></span>
          <span
            class="page-btn"
            :class="{ disabled: currentPage === totalPages }"
            @click="currentPage < totalPages && (currentPage++)"
          >
            下一页 &raquo;
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  top: { type: Number, default: 0 },
  left: { type: Number, default: 0 }
})

const emit = defineEmits(['select', 'close'])

const tabs = [
  { key: 'hot', label: '热门' },
  { key: 'ABCDE', label: 'ABCDE' },
  { key: 'FGHIJ', label: 'FGHIJ' },
  { key: 'KLMNO', label: 'KLMNO' },
  { key: 'PQRST', label: 'PQRST' },
  { key: 'UVWXYZ', label: 'UVWXYZ' }
]

const currentTab = ref('hot')
const currentPage = ref(1)
const itemsPerLetterPage = 12 // 2 rows of 6

const hotCities = [
  { name: '北京', code: 'BJP' }, { name: '上海', code: 'SHH' }, { name: '天津', code: 'TJP' },
  { name: '重庆', code: 'CQW' }, { name: '长沙', code: 'CSQ' }, { name: '长春', code: 'CCT' },
  { name: '成都', code: 'CDW' }, { name: '福州', code: 'FZS' }, { name: '广州', code: 'GZQ' },
  { name: '贵阳', code: 'GIW' }, { name: '呼和浩特', code: 'HHC' }, { name: '哈尔滨', code: 'HBB' },
  { name: '合肥', code: 'HFH' }, { name: '杭州', code: 'HZH' }, { name: '海口', code: 'VUQ' },
  { name: '济南', code: 'JNK' }, { name: '昆明', code: 'KMM' }, { name: '拉萨', code: 'LSO' },
  { name: '兰州', code: 'LZJ' }, { name: '南宁', code: 'NNZ' }, { name: '南京', code: 'NJH' },
  { name: '南昌', code: 'NCG' }, { name: '沈阳', code: 'SYT' }, { name: '石家庄', code: 'SJP' },
  { name: '太原', code: 'TYV' }, { name: '乌鲁木齐南', code: 'WMR' }, { name: '武汉', code: 'WHN' },
  { name: '西宁', code: 'XNO' }, { name: '西安', code: 'XAY' }, { name: '银川', code: 'YIJ' },
  { name: '郑州', code: 'ZZF' }, { name: '深圳', code: 'SZQ' }, { name: '厦门', code: 'XMS' }
]

const cityData = {
  ABCDE: {
    A: [{ name: '昂昂溪', code: 'AAX' }, { name: '阿城北', code: 'ABB' }, { name: '阿城', code: 'ACB' }, { name: '安次', code: 'ACI' }, { name: '安达', code: 'ADX' }, { name: '安德', code: 'ARW' }, { name: '阿尔山北', code: 'ARX' }, { name: '阿尔山', code: 'ART' }, { name: '安吉', code: 'AJU' }, { name: '安靖', code: 'PYW' }, { name: '安家', code: 'AJB' }, { name: '安康', code: 'AKY' }, { name: '昂昂溪', code: 'AAX' }, { name: '阿城北', code: 'ABB' }, { name: '阿城', code: 'ACB' }, { name: '安次', code: 'ACI' }, { name: '安达', code: 'ADX' }, { name: '安德', code: 'ARW' }],
    B: [{ name: '北京北', code: 'VAP' }, { name: '北京东', code: 'BOP' }, { name: '北京', code: 'BJP' }, { name: '北京南', code: 'VNP' }, { name: '北京大兴', code: 'IPP' }, { name: '北京西', code: 'BXP' }, { name: '北京朝阳', code: 'IFP' }, { name: '滨江', code: 'BJB' }, { name: '百浪', code: 'BRZ' }, { name: '班猫箐', code: 'BNM' }, { name: '北营', code: 'BIV' }, { name: '北安', code: 'BAB' }, { name: '北京北', code: 'VAP' }, { name: '北京东', code: 'BOP' }, { name: '北京', code: 'BJP' }, { name: '北京南', code: 'VNP' }],
    C: [{ name: '重庆北', code: 'CUW' }, { name: '重庆东', code: 'COE' }, { name: '重庆', code: 'CQW' }, { name: '重庆南', code: 'CRW' }, { name: '重庆西', code: 'CXW' }, { name: '长春', code: 'CCT' }, { name: '长春南', code: 'CET' }, { name: '长春西', code: 'CRT' }, { name: '成都东', code: 'ICW' }, { name: '成都南', code: 'CNW' }, { name: '成都', code: 'CDW' }, { name: '成都西', code: 'CMW' }, { name: '重庆北', code: 'CUW' }, { name: '重庆东', code: 'COE' }, { name: '重庆', code: 'CQW' }, { name: '重庆南', code: 'CRW' }],
    D: [{ name: '大成', code: 'DCT' }, { name: '大拟', code: 'DNZ' }, { name: '读书铺', code: 'DPM' }, { name: '大王滩', code: 'DZZ' }, { name: '大元', code: 'DYZ' }, { name: '大安北', code: 'RNT' }, { name: '东安东', code: 'DCZ' }, { name: '达坂城', code: 'DCR' }, { name: '定边', code: 'DYJ' }, { name: '东岔', code: 'DCJ' }, { name: '丹东', code: 'DUT' }, { name: '东方', code: 'UFQ' }, { name: '大成', code: 'DCT' }, { name: '大拟', code: 'DNZ' }, { name: '读书铺', code: 'DPM' }, { name: '大王滩', code: 'DZZ' }],
    E: [{ name: '峨边南', code: 'ENE' }, { name: '鄂尔多斯', code: 'EEC' }, { name: '额济纳', code: 'EJC' }, { name: '二连', code: 'RLC' }, { name: '峨眉', code: 'EMW' }, { name: '峨眉山', code: 'IXW' }, { name: '恩施', code: 'ESN' }, { name: '鄂州', code: 'ECN' }, { name: '二道沟门', code: 'RDP' }, { name: '二道湾', code: 'RDX' }, { name: '二龙山屯', code: 'ELA' }, { name: '二密河', code: 'RML' }, { name: '峨边南', code: 'ENE' }, { name: '鄂尔多斯', code: 'EEC' }, { name: '额济纳', code: 'EJC' }, { name: '二连', code: 'RLC' }]
  },
  FGHIJ: {
    F: [{ name: '丰水村', code: 'FSJ' }, { name: '福州', code: 'FZS' }, { name: '福州南', code: 'FYS' }, { name: '防城港北', code: 'FBZ' }, { name: '福鼎', code: 'FES' }, { name: '肥东', code: 'FIH' }, { name: '丰都', code: 'FUW' }, { name: '发耳', code: 'FEM' }, { name: '府谷', code: 'FUV' }, { name: '福海', code: 'FHR' }, { name: '凤凰机场', code: 'FJQ' }, { name: '凤凰城', code: 'FHT' }, { name: '丰水村', code: 'FSJ' }, { name: '福州', code: 'FZS' }, { name: '福州南', code: 'FYS' }, { name: '防城港北', code: 'FBZ' }],
    G: [{ name: '甘草店', code: 'GDJ' }, { name: '钢城', code: 'GAK' }, { name: '孤家子', code: 'GKT' }, { name: '广南卫', code: 'GNM' }, { name: '贵阳', code: 'GIW' }, { name: '贵阳北', code: 'KQW' }, { name: '贵阳东', code: 'KEW' }, { name: '广州北', code: 'GBQ' }, { name: '广州', code: 'GZQ' }, { name: '广州东', code: 'GGQ' }, { name: '广州南', code: 'IZQ' }, { name: '广州新塘', code: 'XWQ' }, { name: '甘草店', code: 'GDJ' }, { name: '钢城', code: 'GAK' }, { name: '孤家子', code: 'GKT' }, { name: '广南卫', code: 'GNM' }],
    H: [{ name: '哈尔滨北', code: 'HTB' }, { name: '哈尔滨', code: 'HBB' }, { name: '哈尔滨东', code: 'VBB' }, { name: '哈尔滨西', code: 'VAB' }, { name: '合肥北城', code: 'COH' }, { name: '合肥', code: 'HFH' }, { name: '合肥南', code: 'ENH' }, { name: '皇姑屯', code: 'HTT' }, { name: '呼和浩特东', code: 'NDC' }, { name: '呼和浩特', code: 'HHC' }, { name: '海口东', code: 'HMQ' }, { name: '海口', code: 'VUQ' }, { name: '哈尔滨北', code: 'HTB' }, { name: '哈尔滨', code: 'HBB' }, { name: '哈尔滨东', code: 'VBB' }, { name: '哈尔滨西', code: 'VAB' }],
    J: [{ name: '金马村', code: 'JMM' }, { name: '济南', code: 'JNK' }, { name: '济南东', code: 'MDK' }, { name: '济南西', code: 'JGK' }, { name: '吉安', code: 'VAG' }, { name: '集安', code: 'JAL' }, { name: '建安', code: 'JUL' }, { name: '吉安西', code: 'JIG' }, { name: '江边村', code: 'JBG' }, { name: '晋城东', code: 'JGF' }, { name: '金昌', code: 'JCJ' }, { name: '晋城', code: 'JCF' }, { name: '金马村', code: 'JMM' }, { name: '济南', code: 'JNK' }, { name: '济南东', code: 'MDK' }, { name: '济南西', code: 'JGK' }]
  },
  KLMNO: {
    K: [{ name: '昆明', code: 'KMM' }, { name: '昆明南', code: 'KOM' }, { name: '开安', code: 'KAT' }, { name: '库车', code: 'KCR' }, { name: '库都尔', code: 'KDX' }, { name: '库尔勒', code: 'KLR' }, { name: '开封北', code: 'KBF' }, { name: '开封', code: 'KFF' }, { name: '开福寺', code: 'FLQ' }, { name: '开化', code: 'KHU' }, { name: '康金井', code: 'KJB' }, { name: '岢岚', code: 'KLV' }, { name: '昆明', code: 'KMM' }, { name: '昆明南', code: 'KOM' }, { name: '开安', code: 'KAT' }, { name: '库车', code: 'KCR' }],
    L: [{ name: '礼贤', code: 'LXI' }, { name: '练塘', code: 'LTU' }, { name: '历城', code: 'VHK' }, { name: '蔺家楼', code: 'ULK' }, { name: '龙泉寺', code: 'UQJ' }, { name: '拉萨', code: 'LSO' }, { name: '乐善村', code: 'LUM' }, { name: '林盛堡', code: 'LBT' }, { name: '骆驼巷', code: 'LTJ' }, { name: '莱芜北', code: 'VIK' }, { name: '兰州东', code: 'LVJ' }, { name: '兰州', code: 'LZJ' }, { name: '礼贤', code: 'LXI' }, { name: '练塘', code: 'LTU' }, { name: '历城', code: 'VHK' }, { name: '蔺家楼', code: 'ULK' }],
    M: [{ name: '茂舍祖', code: 'MOM' }, { name: '马鞍山东', code: 'OMH' }, { name: '麻城北', code: 'MBN' }, { name: '麻城', code: 'MCN' }, { name: '渑池南', code: 'MNF' }, { name: '免渡河', code: 'MDX' }, { name: '牡丹江', code: 'MDB' }, { name: '莫尔道嘎', code: 'MRX' }, { name: '帽儿山', code: 'MRB' }, { name: '帽儿山西', code: 'MUB' }, { name: '明光', code: 'MGH' }, { name: '满归', code: 'MHX' }, { name: '茂舍祖', code: 'MOM' }, { name: '马鞍山东', code: 'OMH' }, { name: '麻城北', code: 'MBN' }, { name: '麻城', code: 'MCN' }],
    N: [{ name: '南昌东', code: 'NUG' }, { name: '南昌', code: 'NCG' }, { name: '南昌南', code: 'HOG' }, { name: '宁村', code: 'NCZ' }, { name: '南昌西', code: 'NXG' }, { name: '南京', code: 'NJH' }, { name: '南京南', code: 'NKH' }, { name: '那罗', code: 'ULZ' }, { name: '南宁北', code: 'NRZ' }, { name: '南宁东', code: 'NFZ' }, { name: '南宁', code: 'NNZ' }, { name: '南宁西', code: 'NXZ' }, { name: '南昌东', code: 'NUG' }, { name: '南昌', code: 'NCG' }, { name: '南昌南', code: 'HOG' }, { name: '宁村', code: 'NCZ' }]
  },
  PQRST: {
    P: [{ name: '坡底下', code: 'PXJ' }, { name: '普安', code: 'PAN' }, { name: '蒲城东', code: 'PEY' }, { name: '平昌', code: 'PCE' }, { name: '平定', code: 'PIP' }, { name: '平顶山', code: 'PEN' }, { name: '平度', code: 'PNK' }, { name: '平度西', code: 'PAK' }, { name: '平顶山西', code: 'PDF' }, { name: '普洱', code: 'PEM' }, { name: '平房', code: 'PFB' }, { name: '盘锦北', code: 'PBD' }, { name: '坡底下', code: 'PXJ' }, { name: '普安', code: 'PAN' }, { name: '蒲城东', code: 'PEY' }, { name: '平昌', code: 'PCE' }],
    Q: [{ name: '七甸', code: 'QDM' }, { name: '庆安', code: 'QAB' }, { name: '青白江东', code: 'QFW' }, { name: '清城', code: 'QCA' }, { name: '蕲春', code: 'QRN' }, { name: '青川', code: 'QCE' }, { name: '黔城', code: 'QEQ' }, { name: '青城山', code: 'QSW' }, { name: '青岛', code: 'QDK' }, { name: '青岛北', code: 'QHK' }, { name: '千岛湖', code: 'QDU' }, { name: '启东', code: 'QOU' }, { name: '七甸', code: 'QDM' }, { name: '庆安', code: 'QAB' }, { name: '青白江东', code: 'QFW' }, { name: '清城', code: 'QCA' }],
    R: [{ name: '融安', code: 'RAZ' }, { name: '瑞安', code: 'RAH' }, { name: '荣昌北', code: 'RQW' }, { name: '荣成', code: 'RCK' }, { name: '如东', code: 'RIH' }, { name: '汝箕沟', code: 'RQJ' }, { name: '瑞金', code: 'RJG' }, { name: '日喀则', code: 'RKO' }, { name: '饶平', code: 'RVQ' }, { name: '若羌', code: 'RQR' }, { name: '乳山南', code: 'REK' }, { name: '日照', code: 'RZK' }, { name: '融安', code: 'RAZ' }, { name: '瑞安', code: 'RAH' }, { name: '荣昌北', code: 'RQW' }, { name: '荣成', code: 'RCK' }],
    S: [{ name: '上海', code: 'SHH' }, { name: '上海南', code: 'SNH' }, { name: '上海虹桥', code: 'AOH' }, { name: '上海西', code: 'SXH' }, { name: '世博园', code: 'ZWT' }, { name: '石家庄北', code: 'VVP' }, { name: '石家庄东', code: 'SXP' }, { name: '邵家堂', code: 'SJJ' }, { name: '石家庄', code: 'SJP' }, { name: '施家嘴', code: 'SHM' }, { name: '沈阳', code: 'SYT' }, { name: '沈阳北', code: 'SBT' }, { name: '上海', code: 'SHH' }, { name: '上海南', code: 'SNH' }, { name: '上海虹桥', code: 'AOH' }, { name: '上海西', code: 'SXH' }]
  },
  UVWXYZ: {
    W: [{ name: '武汉', code: 'WHN' }, { name: '武汉东', code: 'LFN' }, { name: '王家湾', code: 'WJJ' }, { name: '乌鲁木齐南', code: 'WMR' }, { name: '乌鲁木齐', code: 'WAR' }, { name: '吴圩机场', code: 'WJZ' }, { name: '王兆屯', code: 'WZB' }, { name: '文昌', code: 'WEQ' }, { name: '武昌', code: 'WCN' }, { name: '五常', code: 'WCB' }, { name: '武当山', code: 'WRN' }, { name: '潍坊', code: 'WFK' }, { name: '武汉', code: 'WHN' }, { name: '武汉东', code: 'LFN' }, { name: '王家湾', code: 'WJJ' }, { name: '乌鲁木齐南', code: 'WMR' }],
    X: [{ name: '西安北', code: 'EAY' }, { name: '西安', code: 'XAY' }, { name: '西固城', code: 'XUJ' }, { name: '西街口', code: 'EKM' }, { name: '许家台', code: 'XTJ' }, { name: '西宁', code: 'XNO' }, { name: '小哨', code: 'XAM' }, { name: '雪野', code: 'XYK' }, { name: '兴安北', code: 'XDZ' }, { name: '雄安', code: 'IQP' }, { name: '西安西', code: 'EGY' }, { name: '许昌东', code: 'XVF' }, { name: '西安北', code: 'EAY' }, { name: '西安', code: 'XAY' }, { name: '西固城', code: 'XUJ' }, { name: '西街口', code: 'EKM' }],
    Y: [{ name: '银川', code: 'YIJ' }, { name: '永丰营', code: 'YYM' }, { name: '宜耐', code: 'YVM' }, { name: '羊堡', code: 'ABM' }, { name: '榆树台', code: 'YUT' }, { name: '引镇', code: 'CAY' }, { name: '雅安', code: 'YAE' }, { name: '延安', code: 'YWY' }, { name: '永安南', code: 'YQS' }, { name: '依安', code: 'YAX' }, { name: '迎宾路', code: 'YFW' }, { name: '亚布力', code: 'YBB' }, { name: '银川', code: 'YIJ' }, { name: '永丰营', code: 'YYM' }, { name: '宜耐', code: 'YVM' }, { name: '羊堡', code: 'ABM' }],
    Z: [{ name: '朱家窑', code: 'ZUJ' }, { name: '章丘南', code: 'VQK' }, { name: '郑州东', code: 'ZAF' }, { name: '郑州航空港', code: 'ZIF' }, { name: '郑州', code: 'ZZF' }, { name: '郑州西', code: 'XPF' }, { name: '诏安', code: 'ZDS' }, { name: '淄博北', code: 'ZRK' }, { name: '淄博', code: 'ZBK' }, { name: '镇城底', code: 'ZDV' }, { name: '正定机场', code: 'ZHP' }, { name: '正定', code: 'ZDP' }, { name: '朱家窑', code: 'ZUJ' }, { name: '章丘南', code: 'VQK' }, { name: '郑州东', code: 'ZAF' }, { name: '郑州航空港', code: 'ZIF' }]
  }
}

const totalPages = computed(() => {
  if (currentTab.value === 'hot') return 1
  const groups = cityData[currentTab.value] || {}
  let maxLen = 0
  for (const letter in groups) {
    if (groups[letter].length > maxLen) {
      maxLen = groups[letter].length
    }
  }
  return Math.ceil(maxLen / itemsPerLetterPage)
})

const currentCitiesGroup = computed(() => {
  if (currentTab.value === 'hot') return {}
  
  const groups = cityData[currentTab.value] || {}
  const pagedGroups = {}
  
  for (const letter in groups) {
    const start = (currentPage.value - 1) * itemsPerLetterPage
    const end = start + itemsPerLetterPage
    pagedGroups[letter] = groups[letter].slice(start, end)
  }
  
  return pagedGroups
})

const selectCity = (city) => {
  emit('select', city.name)
  emit('close')
}

watch(currentTab, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.city-selector {
  position: absolute;
  width: 580px;
  background: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 2000;
  font-size: 12px;
  display: flex;
  font-family: 'Microsoft YaHei', sans-serif;
}

/* Sidebar Styles */
.city-selector-sidebar {
  width: 90px;
  background-color: #f8f8f8;
  border-right: 1px solid #eee;
  flex-shrink: 0;
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-item {
  width: 76px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  cursor: pointer;
  color: #333;
  margin-bottom: 5px;
  border-radius: 4px;
}

.sidebar-item:hover {
  background-color: #eee;
}

.sidebar-item.active {
  background-color: #3B99FC;
  color: #fff;
}

/* Main Content Styles */
.city-selector-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.city-selector-header {
  padding: 10px 15px;
  color: #666;
  border-bottom: 1px solid #eee;
}

/* Tabs Styles */
.city-selector-tabs {
  display: flex;
  background: #EAF4FF;
  padding: 0 10px;
}

.city-selector-tab {
  padding: 8px 15px;
  cursor: pointer;
  color: #333;
  border-bottom: 2px solid transparent; /* Reserve space for border */
  margin-bottom: -1px; /* Align with bottom */
}

.city-selector-tab.active {
  color: #3B99FC;
  border-bottom: 2px solid #3B99FC;
  font-weight: bold;
}

.city-selector-tab:hover {
  color: #3B99FC;
}

/* Content Styles */
.city-selector-content {
  padding: 10px 15px;
  min-height: 200px;
  background: #fff;
}

.city-list {
  display: flex;
  flex-wrap: wrap;
}

.city-item {
  width: 16.66%; /* 6 items per row */
  height: 24px;
  line-height: 24px;
  cursor: pointer;
  color: #333;
  padding-left: 5px;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.city-item:hover {
  background-color: #3B99FC;
  color: #fff;
  border-radius: 2px;
}

/* Grouped List Styles */
.city-group-row {
  display: flex;
  margin-bottom: 5px;
}

.city-group-letter {
  width: 30px;
  font-weight: bold;
  color: #3B99FC;
  text-align: center;
  padding-top: 2px;
  flex-shrink: 0;
}

.city-group-list {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
}

/* Footer Styles */
.city-selector-footer {
  padding: 5px 10px;
  text-align: right;
  border-top: 1px solid #eee;
}

.pagination-controls {
  display: inline-block;
}

.page-btn {
  display: inline-block;
  padding: 2px 8px;
  margin-left: 10px;
  cursor: pointer;
  color: #333;
}

.page-btn:hover {
  color: #3B99FC;
  text-decoration: underline;
}

.page-btn.disabled {
  color: #ccc;
  cursor: not-allowed;
  text-decoration: none;
}
</style>

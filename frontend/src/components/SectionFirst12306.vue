<template>
  <div class="section-first">
    <!-- 轮播图 -->
    <div class="fullSlide">
      <div class="bd" :style="bdStyle">
        <ul
          class="sowingMap"
          :style="{
            width: slideWidth * extendedSlides.length + 'px',
            position: 'absolute',
            top: '0',
            left: -currentIndex * slideWidth + 'px',
            padding: '0',
            margin: '0',
            transition: transitionEnabled ? 'all 0.4s ease' : 'none'
          }"
          @mouseenter="pauseAuto"
          @mouseleave="resumeAuto"
        >
          <li
            v-for="(img, idx) in extendedSlides"
            :key="'slide-' + idx"
            :style="{
              background: `url(${img}) center center no-repeat`,
              float: 'left',
              width: slideWidth + 'px',
              height: '450px'
            }"
          >
            <a :href="linkFor(idx)" target="_blank"></a>
          </li>
        </ul>
      </div>
      <div class="hd">
        <ul>
          <li
            v-for="(img, idx) in slides"
            :key="'indicator-' + idx"
            :class="{ on: indicatorIndex === idx }"
            @click="goSlide(idx)"
          ></li>
        </ul>
      </div>
    </div>

    <!-- 查询框 -->
    <div class="search-index">
      <!-- 左侧菜单 -->
      <ul class="search-side">
        <li :class="{ active: activeSide === 'ticket' }" @click="setSide('ticket')">
          <a href="javascript:;">
            <i class="icon icon-huochepiao"></i>
            车票
          </a>
        </li>
        <li :class="{ active: activeSide === 'common' }" @click="setSide('common')">
          <a href="javascript:;">
            <i class="icon icon-cycx"></i>
            常用查询
          </a>
        </li>
        <li :class="['last', { active: activeSide === 'cater' }]" @click="setSide('cater')">
          <a href="javascript:;">
            <i class="icon icon-dingcan"></i>
            订餐
          </a>
        </li>
      </ul>

      <!-- 右侧内容 -->
      <div class="search-main">
        <!-- 车票查询 -->
        <div class="search-main-item" v-show="activeSide === 'ticket'">
          <div class="search-main-tab">
            <div class="search-tab-hd">
              <ul>
                <li :class="{ active: activeTab === 'single' }">
                  <a href="javascript:void(0)" @click="activeTab = 'single'">
                    <i class="icon icon-dancheng"></i>
                    单程
                  </a>
                </li>
                <li :class="{ active: activeTab === 'round' }">
                  <a href="javascript:void(0)" @click="activeTab = 'round'">
                    <i class="icon icon-wangfan"></i>
                    往返
                  </a>
                </li>
                <li :class="{ active: activeTab === 'transfer' }">
                  <a href="javascript:void(0)" @click="activeTab = 'transfer'">
                    <i class="icon icon-huancheng"></i>
                    中转换乘
                  </a>
                </li>
                <li :class="{ active: activeTab === 'change' }">
                  <a href="javascript:void(0)" @click="activeTab = 'change'">
                    <i class="icon icon-chepiao"></i>
                    退改签
                  </a>
                </li>
              </ul>
            </div>

            <div class="search-tab-bd">
              <!-- 单程 -->
              <div class="search-tab-item" :class="{ active: activeTab === 'single' }">
                <div class="search-form">
                  <div class="form-item-group">
                    <div class="form-item">
                      <label for="fromStationText" class="form-label">出发地</label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="fromStation" type="hidden" name="from_station" />
                          <input
                            type="text"
                            class="input"
                            v-model="single.fromStation"
                            id="fromStationText"
                            autocomplete="off"
                            aria-label="请输入或选择出发地，按键盘上下键进行选择，按回车键选中"
                            @click="showCitySelector('single.from', $event)"
                            @input="handleInput('single.from', $event)"
                          />
                          <i class="icon icon-place" data-click="fromStationText" @click.stop="showCitySelector('single.from', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="form-item">
                      <label for="toStationText" class="form-label">到达地</label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="toStation" type="hidden" name="to_station" />
                          <input
                            type="text"
                            class="input"
                            v-model="single.toStation"
                            id="toStationText"
                            autocomplete="off"
                            aria-label="请输入或选择到达地，按键盘上下键进行选择，按回车键选中"
                            @click="showCitySelector('single.to', $event)"
                            @input="handleInput('single.to', $event)"
                          />
                          <i class="icon icon-place" data-click="toStationText" @click.stop="showCitySelector('single.to', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="city-change">
                      <i
                        class="icon icon-qiehuan"
                        title="切换"
                        id="danChange"
                        @click="swapStations('single')"
                      ></i>
                    </div>
                  </div>

                  <div class="form-item">
                    <label for="train_date" class="form-label">出发日期</label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input
                          type="text"
                          class="input"
                          v-model="single.date"
                          id="train_date"
                          autocomplete="off"
                          aria-label="请输入日期，例如2021杠01杠01"
                          @click="showDateSelector('train_date', 'single.date', $event)"
                          readonly
                          style="cursor: pointer;"
                        />
                        <i class="icon icon-date" data-click="train_date"></i>
                      </div>
                    </div>
                  </div>

                  <div class="form-item form-item-check">
                    <div class="form-bd">
                      <ul class="check-list check-list-right">
                        <li id="isStudentDan" @click="single.student = !single.student">
                          学生
                          <i></i>
                        </li>
                        <li id="isHighDan" @click="single.highSpeed = !single.highSpeed">
                          高铁/动车
                          <i></i>
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div class="form-item form-item-btn">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="search_one"
                      @click="submitSingle"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>

                <div id="search-history" style="display: block">
                  <div class="search-history-bd">
                    <i
                      id="iconLeftHos"
                      class="history-prev icon icon-caret-left"
                      @click="prevHistory"
                    ></i>
                    <i
                      id="iconRightHos"
                      class="history-next icon icon-caret-right"
                      @click="nextHistory"
                    ></i>
                    <div class="history-list-wrap">
                      <ul class="history-list" id="history_ul" style="position: relative">
                        <li v-for="(h, i) in showHistory" :key="i" @click="applyHistory(h)">
                          {{ h }}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="search-history-btn">
                    <a href="javascript:void(0)" @click="clearHistory">删除历史</a>
                  </div>
                </div>
              </div>

              <!-- 往返 -->
              <div class="search-tab-item" :class="{ active: activeTab === 'round' }">
                <div class="search-form">
                  <div class="form-item-group">
                    <div class="form-item">
                      <label for="fromStationFanText" class="form-label">出发地</label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="fromStationFan" type="hidden" name="from_station_fan" />
                          <input
                            type="text"
                            class="input"
                            v-model="round.fromStation"
                            id="fromStationFanText"
                            autocomplete="off"
                            aria-label="请输入或选择出发地，按键盘上下键进行选择，按回车键选中"
                            @click="showCitySelector('round.from', $event)"
                            @input="handleInput('round.from', $event)"
                          />
                          <i class="icon icon-place" data-click="fromStationFanText" @click.stop="showCitySelector('round.from', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="form-item">
                      <label for="toStationFanText" class="form-label">到达地</label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="toStationFan" type="hidden" name="to_station_fan" />
                          <input
                            type="text"
                            class="input"
                            v-model="round.toStation"
                            id="toStationFanText"
                            autocomplete="off"
                            aria-label="请输入或选择到达地，按键盘上下键进行选择，按回车键选中"
                            @click="showCitySelector('round.to', $event)"
                            @input="handleInput('round.to', $event)"
                          />
                          <i class="icon icon-place" data-click="toStationFanText" @click.stop="showCitySelector('round.to', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="city-change">
                      <i
                        class="icon icon-qiehuan"
                        title="切换"
                        id="returnChange"
                        @click="swapStations('round')"
                      ></i>
                    </div>
                  </div>

                  <div class="form-item">
                    <label for="go_date" class="form-label">出发日期</label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input
                          type="text"
                          class="input"
                          v-model="round.goDate"
                          id="go_date"
                          aria-label="请输入日期，例如2021杠01杠01"
                          @click="showDateSelector('go_date', 'round.goDate', $event)"
                          readonly
                          style="cursor: pointer;"
                        />
                        <i class="icon icon-date" data-click="go_date"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="from_date" class="form-label">返程日期</label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input
                          type="text"
                          class="input"
                          v-model="round.backDate"
                          id="from_date"
                          aria-label="请输入日期，例如2021杠01杠01"
                          @click="showDateSelector('from_date', 'round.backDate', $event)"
                          readonly
                          style="cursor: pointer;"
                        />
                        <i class="icon icon-date" data-click="from_date"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-check">
                    <div class="form-bd">
                      <ul class="check-list check-list-right">
                        <li id="isStudent" @click="round.student = !round.student">
                          学生
                          <i></i>
                        </li>
                        <li id="isHigh" @click="round.highSpeed = !round.highSpeed">
                          高铁/动车
                          <i></i>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="form-item form-item-btn">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="search_two"
                      @click="submitRound"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>

              <!-- 接续换乘（展示为占位） -->
              <div class="search-tab-item" :class="{ active: activeTab === 'transfer' }">
                <div class="search-form">
                  <div class="form-item-group">
                    <div class="form-item">
                      <label for="fromStationSerialText" class="form-label">
                        <b class="required">*</b>
                        出发地
                      </label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="fromStationSerial" type="hidden" name="from_station_serial" />
                          <input
                            type="text"
                            class="input"
                            id="fromStationSerialText"
                            v-model="transfer.fromStation"
                            autocomplete="off"
                            @click="showCitySelector('transfer.from', $event)"
                            @input="handleInput('transfer.from', $event)"
                          />
                          <i class="icon icon-place" data-click="fromStationSerialText" @click.stop="showCitySelector('transfer.from', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="form-item">
                      <label for="toStationSerialText" class="form-label">
                        <b class="required">*</b>
                        到达地
                      </label>
                      <div class="form-bd">
                        <div class="input-box input-city">
                          <input id="toStationSerial" type="hidden" name="to_station_serial" />
                          <input
                            type="text"
                            class="input"
                            id="toStationSerialText"
                            v-model="transfer.toStation"
                            autocomplete="off"
                            @click="showCitySelector('transfer.to', $event)"
                            @input="handleInput('transfer.to', $event)"
                          />
                          <i class="icon icon-place" data-click="toStationSerialText" @click.stop="showCitySelector('transfer.to', $event)"></i>
                        </div>
                      </div>
                    </div>
                    <div class="city-change">
                      <i
                        class="icon icon-qiehuan"
                        title="切换"
                        id="serialChange"
                        @click="swapStations('transfer')"
                      ></i>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="serial_date" class="form-label">
                      <b class="required">*</b>
                      乘车日期
                    </label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input type="text" class="input" id="serial_date" v-model="transfer.date" />
                        <i class="icon icon-date" data-click="serial_date"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-check">
                    <div class="form-bd">
                      <ul class="check-list check-list-right">
                        <li id="isStudentLian" @click="transfer.student = !transfer.student">
                          学生
                          <i></i>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="form-item form-item-btn">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="search_three"
                      @click="submitTransfer"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>

              <!-- 退改签（占位展示） -->
              <div class="search-tab-item" :class="{ active: activeTab === 'change' }">
                <div class="search-form">
                  <div class="form-item">
                    <span class="form-label">查询类型</span>
                    <div class="form-bd">
                      <ul class="radio-list radio-list-ding">
                        <li
                          id="dingqiaoID"
                          :class="{ active: change.type === 'order' }"
                          @click="change.type = 'order'"
                        >
                          <i></i>
                          订票日期
                        </li>
                        <li
                          :class="{ active: change.type === 'ride' }"
                          @click="change.type = 'ride'"
                        >
                          <i></i>
                          乘车日期
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="refund_start" class="form-label">
                      <b class="required">*</b>
                      开始日期
                    </label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input
                          type="text"
                          class="input"
                          id="refund_start"
                          v-model="change.startDate"
                        />
                        <i class="icon icon-date" data-click="refund_start"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="refund_end" class="form-label">
                      <b class="required">*</b>
                      结束日期
                    </label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input type="text" class="input" id="refund_end" v-model="change.endDate" />
                        <i class="icon icon-date" data-click="refund_end"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="refund_code" class="form-label">
                      <b class="required"></b>
                      关键字
                    </label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input
                          type="text"
                          class="input search-input"
                          id="refund_code"
                          placeholder="订单号/车次/乘客姓名"
                          v-model="change.keyword"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg">
                    <a
                      href="javascript:;"
                      class="btn btn-primary form-block"
                      id="refund_button"
                      @click="submitChange"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 常用查询 -->
        <div class="search-main-item" v-show="activeSide === 'common'">
          <div class="search-main-tab">
            <div class="search-tab-hd">
              <ul>
                <li :class="{ active: activeCommonTab === 'zwd' }">
                  <a href="javascript:void(0)" @click="activeCommonTab = 'zwd'">
                    <i class="icon icon-shijian"></i>
                    正晚点
                  </a>
                </li>
                <li :class="{ active: activeCommonTab === 'checkin' }">
                  <a href="javascript:void(0)" @click="activeCommonTab = 'checkin'">
                    <i class="icon icon-jianpiaokou"></i>
                    检票口
                  </a>
                </li>
                <li :class="{ active: activeCommonTab === 'sale' }">
                  <a href="javascript:void(0)" @click="activeCommonTab = 'sale'">
                    <i class="icon icon-qishou"></i>
                    起售时间
                  </a>
                </li>
                <li :class="{ active: activeCommonTab === 'weather' }">
                  <a href="javascript:void(0)" @click="activeCommonTab = 'weather'">
                    <i class="icon icon-tianqi"></i>
                    天气查询
                  </a>
                </li>
              </ul>
            </div>
            <div class="search-tab-bd">
              <!-- 正晚点 -->
              <div class="search-tab-item" :class="{ active: activeCommonTab === 'zwd' }">
                <div class="search-form">
                  <div class="form-item">
                    <span class="form-label">查询类型</span>
                    <div class="form-bd">
                      <ul class="radio-list radio-list-station">
                        <li
                          id="destination_station"
                          :class="{ active: commonZwd.type === 'arrival' }"
                          @click="commonZwd.type = 'arrival'"
                        >
                          <i></i>
                          到达站
                        </li>
                        <li
                          :class="{ active: commonZwd.type === 'departure' }"
                          @click="commonZwd.type = 'departure'"
                        >
                          <i></i>
                          出发站
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="stationValueText" class="form-label">车站</label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input id="stationValue" type="hidden" name="stationValue" />
                        <input
                          type="text"
                          class="input"
                          id="stationValueText"
                          placeholder="简拼／全拼／汉字"
                          autocomplete="off"
                          v-model="commonZwd.station"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="numberValue" class="form-label">车次</label>
                    <div class="form-bd">
                      <div class="input-box late_poit">
                        <input
                          type="text"
                          class="input"
                          placeholder="请输入车次"
                          id="numberValue"
                          autocomplete="off"
                          v-model="commonZwd.trainNo"
                        />
                        <ul
                          class="active"
                          name="makeupCoSe"
                          id="train_hide"
                          style="width: 270px; z-index: 1"
                        ></ul>
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg">
                    <a href="javascript:void(0)" class="btn btn-primary form-block" id="bie_button">
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>

              <!-- 检票口 -->
              <div class="search-tab-item" :class="{ active: activeCommonTab === 'checkin' }">
                <div class="search-form">
                  <div class="form-item">
                    <label for="check_in" class="form-label">
                      <b class="required">*</b>
                      乘车日期
                    </label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input type="text" class="input" id="check_in" />
                        <i class="icon icon-date" data-click="check_in"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="train_num" class="form-label">
                      <b class="required">*</b>
                      车次
                    </label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input
                          type="text"
                          class="input search-input"
                          placeholder="请输入车次"
                          autocomplete="off"
                          id="train_num"
                          style="text-transform: uppercase"
                        />
                        <input class="input" type="hidden" id="topicId" />
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="ticketEntranceSel" class="form-label">
                      <b class="required">*</b>
                      乘车站
                    </label>
                    <div class="form-bd">
                      <div class="input-box">
                        <div class="model-select-box">
                          <div class="model-select-text" id="ticketEntranceSel" tabindex="0">
                            请选择车站
                          </div>
                          <div
                            class="station-loading"
                            id="station_loading"
                            style="display: none"
                          ></div>
                          <ul
                            class="model-select-option train_hide"
                            id="check_model_select"
                            style="display: none"
                          ></ul>
                          <input
                            type="hidden"
                            class="selected-input"
                            name="cityID"
                            id="selected_input"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg">
                    <a href="javascript:;" class="btn btn-primary form-block" id="check_button">
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>

              <!-- 起售时间 -->
              <div class="search-tab-item" :class="{ active: activeCommonTab === 'sale' }">
                <div class="search-form">
                  <div class="form-item">
                    <label for="sale_time" class="form-label">
                      <b class="required">*</b>
                      起售日期
                    </label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input type="text" class="input" id="sale_time" />
                        <i class="icon icon-date" data-click="sale_time"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="start_sellText" class="form-label">
                      <b class="required">*</b>
                      起售车站
                    </label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input id="start_sell" type="hidden" name="start_sell" />
                        <input type="text" class="input" id="start_sellText" autocomplete="off" />
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="sell_button"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>

              <!-- 天气查询 -->
              <div class="search-tab-item" :class="{ active: activeCommonTab === 'weather' }">
                <div class="search-form">
                  <div class="form-item">
                    <label for="destinationText" class="form-label">
                      <b class="required">*</b>
                      目的地
                    </label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input id="destination" type="hidden" name="destination" />
                        <input
                          type="text"
                          class="input"
                          id="destinationText"
                          placeholder="简拼／全拼／汉字"
                          autocomplete="off"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="weather_button"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 订餐 -->
        <div class="search-main-item" v-show="activeSide === 'cater'">
          <div class="search-main-tab">
            <div class="search-tab-hd">
              <ul>
                <li :class="{ active: activeCaterTab === 'reserve' }" style="width: 50%">
                  <a href="javascript:;" @click="activeCaterTab = 'reserve'">
                    <i class="icon icon-shijian"></i>
                    预订
                  </a>
                </li>
                <li style="width: 50%">
                  <a href="https://exservice.12306.cn/excater/queryMyOrder.html" target="_blank">
                    <i class="icon icon-jianpiaokou"></i>
                    餐饮订单
                  </a>
                </li>
              </ul>
            </div>
            <div class="search-tab-bd">
              <!-- 订餐 -->
              <div
                class="search-tab-item dinner-yuding"
                :class="{ active: activeCaterTab === 'reserve' }"
              >
                <div class="search-form">
                  <div class="form-item">
                    <label for="dinner_date" class="form-label">出发日期</label>
                    <div class="form-bd">
                      <div class="input-box input-data">
                        <input type="text" class="input" id="dinner_date" />
                        <i class="icon icon-date" data-click="dinner_date"></i>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label for="dinner_sub_mun" class="form-label">出发车次</label>
                    <div class="form-bd">
                      <div class="input-box">
                        <input
                          type="text"
                          class="input search-input"
                          placeholder="仅支持G、D字头的动车组列车"
                          autocomplete="off"
                          id="dinner_sub_mun"
                          style="text-transform: uppercase"
                        />
                        <input class="input" type="hidden" id="dinner_sub_code" />
                      </div>
                    </div>
                  </div>
                  <div class="form-item form-item-btn mt-mlg dinner-search">
                    <a
                      href="javascript:void(0)"
                      class="btn btn-primary form-block"
                      id="search_four"
                    >
                      查&nbsp;&nbsp;&nbsp;&nbsp;询
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <CitySelector
        :visible="citySelectorVisible"
        :top="citySelectorTop"
        :left="citySelectorLeft"
        @select="handleCitySelect"
        @close="closeCitySelector"
      />
      <CitySearch
        :visible="citySearchVisible"
        :top="citySelectorTop"
        :left="citySelectorLeft"
        :search-query="searchQuery"
        @select="handleCitySelect"
        @close="closeCitySelector"
      />

      <DateSelector
        :visible="dateSelectorVisible"
        :top="dateSelectorTop"
        :left="dateSelectorLeft"
        :selected-date="getSelectedDate()"
        @select="handleDateSelectorSelect"
        @close="closeDateSelector"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import CitySelector from '@/components/CitySelector.vue'

import CitySearch from '@/components/CitySearch.vue'
import DateSelector from '@/components/DateSelector.vue'
import dayjs from 'dayjs'

const router = useRouter()

// 轮播图片（使用本地副本，路径位于 public/assets/12306/pic）
const slides = ref([
  '/assets/12306/pic/banner12.jpg',
  '/assets/12306/pic/banner20201223.jpg',
  '/assets/12306/pic/banner20200707.jpg',
  '/assets/12306/pic/banner0619.jpg',
  '/assets/12306/pic/banner26.jpg',
  '/assets/12306/pic/banner10.jpg'
])

const slideLinks = ref([
  '',
  'https://kyfw.12306.cn/otn/view/commutation_index.html',
  '',
  '',
  'https://exservice.12306.cn/excater/index.html',
  'https://cx.12306.cn/tlcx/index.html'
])

// 无限循环：首尾克隆
const extendedSlides = computed(() => {
  const s = slides.value
  if (!s.length) return []
  return [s[s.length - 1], ...s, s[0]]
})

const slideWidth = ref(1462)
const currentIndex = ref(1) // 初始指向第一张真实幻灯片
const transitionEnabled = ref(true)
let timer = null

const indicatorIndex = computed(() => {
  const sLen = slides.value.length
  if (currentIndex.value === 0) return sLen - 1
  if (currentIndex.value === sLen + 1) return 0
  return currentIndex.value - 1
})

const linkFor = idx => {
  const sLen = slides.value.length
  if (idx === 0) return slideLinks.value[sLen - 1] || ''
  if (idx === sLen + 1) return slideLinks.value[0] || ''
  return slideLinks.value[idx - 1] || ''
}

const goSlide = idx => {
  transitionEnabled.value = true
  currentIndex.value = idx + 1
}

const nextSlide = () => {
  transitionEnabled.value = true
  currentIndex.value += 1
  const sLen = slides.value.length
  if (currentIndex.value === sLen + 1) {
    setTimeout(() => {
      transitionEnabled.value = false
      currentIndex.value = 1
    }, 420)
  }
}

const pauseAuto = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

const resumeAuto = () => {
  if (!timer) {
    timer = setInterval(nextSlide, 5000)
  }
}

onMounted(() => {
  timer = setInterval(nextSlide, 5000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 使用内联字符串样式以 `!important` 强制容器宽度
const bdStyle = computed(
  () =>
    `width: ${slideWidth.value}px !important; height: 450px; margin: 0 auto; position: relative; overflow: hidden;`
)

// 左侧菜单（默认车票）
const activeSide = ref('ticket')
const setSide = side => {
  activeSide.value = side
  if (side === 'ticket') {
    activeTab.value = 'single'
  } else if (side === 'common') {
    activeCommonTab.value = 'zwd'
  } else if (side === 'cater') {
    activeCaterTab.value = 'reserve'
  }
}

// 查询 Tab
const activeTab = ref('single')

// 单程表单
const single = ref({
  fromStation: '北京',
  toStation: '上海',
  date: new Date().toISOString().slice(0, 10),
  student: false,
  highSpeed: false
})

// 往返表单
const round = ref({
  fromStation: '北京',
  toStation: '上海',
  goDate: new Date().toISOString().slice(0, 10),
  backDate: new Date().toISOString().slice(0, 10),
  student: false,
  highSpeed: false
})

// 接续换乘表单（占位）
const transfer = ref({
  fromStation: '北京',
  toStation: '上海',
  date: new Date().toISOString().slice(0, 10),
  student: false
})

// 退改签查询（占位）
const change = ref({
  type: 'order',
  startDate: new Date().toISOString().slice(0, 10),
  endDate: new Date().toISOString().slice(0, 10),
  keyword: ''
})

// 常用查询子标签
const activeCommonTab = ref('zwd')
const commonZwd = ref({ type: 'arrival', station: '', trainNo: '' })
// 订餐子标签
const activeCaterTab = ref('reserve')

// 历史记录（简单实现）
const history = ref(['北京-上海'])
const showHistory = computed(() => history.value.slice(0, 10))
const applyHistory = h => {
  const [from, to] = h.split('-')
  single.value.fromStation = from
  single.value.toStation = to
}
const clearHistory = () => (history.value = [])
const prevHistory = () => history.value.unshift(history.value.pop())
const nextHistory = () => history.value.push(history.value.shift())

const swapStations = which => {
  if (which === 'single') {
    ;[single.value.fromStation, single.value.toStation] = [
      single.value.toStation,
      single.value.fromStation
    ]
  } else if (which === 'round') {
    ;[round.value.fromStation, round.value.toStation] = [
      round.value.toStation,
      round.value.fromStation
    ]
  } else {
    ;[transfer.value.fromStation, transfer.value.toStation] = [
      transfer.value.toStation,
      transfer.value.fromStation
    ]
  }
}

// 路由提交
const submitSingle = () => {
  const route = `${single.value.fromStation}-${single.value.toStation}`
  if (!history.value.includes(route)) history.value.unshift(route)
  router.push({
    name: 'leftTicket-single',
    query: {
      departure_city: single.value.fromStation,
      arrival_city: single.value.toStation,
      travel_date: single.value.date,
      type: 'single'
    }
  })
}

const submitRound = () => {
  router.push({
    name: 'leftTicket-round',
    query: {
      departure_city: round.value.fromStation,
      arrival_city: round.value.toStation,
      travel_date: round.value.goDate,
      return_date: round.value.backDate,
      type: 'round'
    }
  })
}

const submitTransfer = () => {
  router.push({
    name: 'trains',
    query: {
      departure_city: transfer.value.fromStation,
      arrival_city: transfer.value.toStation,
      travel_date: transfer.value.date,
      type: 'transfer'
    }
  })
}

const submitChange = () => {
  // 跳转至订单查询页，退改签相关功能在此处理
  router.push({ name: 'order-inquiry' })
}

// 城市选择器逻辑
const citySelectorVisible = ref(false)
const citySelectorTop = ref(0)
const citySelectorLeft = ref(0)
const currentSelectingInput = ref('') // 'single.from', 'single.to', 'round.from', etc.

// 城市搜索逻辑
const citySearchVisible = ref(false)
const searchQuery = ref('')

const updatePosition = (event) => {
  let targetEl = event.target
  if (targetEl.tagName === 'I') {
    targetEl = targetEl.previousElementSibling
  }
  const inputBox = targetEl.closest('.input-box')
  if (inputBox) {
    const rect = inputBox.getBoundingClientRect()
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    
    citySelectorTop.value = rect.bottom + scrollTop
    citySelectorLeft.value = rect.left + scrollLeft
  }
}

const showCitySelector = (type, event) => {
  currentSelectingInput.value = type
  searchQuery.value = ''
  citySearchVisible.value = false
  updatePosition(event)
  citySelectorVisible.value = true
}

const handleInput = (type, event) => {
  currentSelectingInput.value = type
  searchQuery.value = event.target.value
  
  if (searchQuery.value) {
    citySelectorVisible.value = false
    updatePosition(event)
    citySearchVisible.value = true
  } else {
    citySearchVisible.value = false
    citySelectorVisible.value = true
  }
}

const handleCitySelect = city => {
  const [mode, field] = currentSelectingInput.value.split('.')
  
  if (mode === 'single') {
    if (field === 'from') single.value.fromStation = city
    else if (field === 'to') single.value.toStation = city
  } else if (mode === 'round') {
    if (field === 'from') round.value.fromStation = city
    else if (field === 'to') round.value.toStation = city
  } else if (mode === 'transfer') {
    if (field === 'from') transfer.value.fromStation = city
    else if (field === 'to') transfer.value.toStation = city
  }
  
  citySelectorVisible.value = false
  citySearchVisible.value = false
}

const closeCitySelector = () => {
  citySelectorVisible.value = false
  citySearchVisible.value = false
}

const handleGlobalClick = (e) => {
  if (citySelectorVisible.value || citySearchVisible.value) {
    const selector = document.querySelector('.city-selector')
    const search = document.querySelector('.city-search')
    const clickedInsideSelector = selector && selector.contains(e.target)
    const clickedInsideSearch = search && search.contains(e.target)
    
    // Check if clicked on any input that triggers city selector
    const isInput = e.target.id && (
      e.target.id === 'fromStationText' || 
      e.target.id === 'toStationText' ||
      e.target.id === 'fromStationFanText' ||
      e.target.id === 'toStationFanText' ||
      e.target.id === 'fromStationSerialText' ||
      e.target.id === 'toStationSerialText'
    )
    
    if (!clickedInsideSelector && !clickedInsideSearch && !isInput) {
      closeCitySelector()
    }
  }
  
  if (dateSelectorVisible.value) {
    const dateSelector = document.querySelector('.cal-wrap')
    const clickedInsideDateSelector = dateSelector && dateSelector.contains(e.target)
    const isInput = e.target.id && (
      e.target.id === 'train_date' ||
      e.target.id === 'go_date' ||
      e.target.id === 'from_date'
    )
    
    if (!clickedInsideDateSelector && !isInput) {
      closeDateSelector()
    }
  }
}

const dateSelectorVisible = ref(false)
const dateSelectorTop = ref(0)
const dateSelectorLeft = ref(0)
const currentSelectingDateInput = ref('')

const showDateSelector = (inputId, modelKey, event) => {
  currentSelectingDateInput.value = modelKey
  const inputEl = document.getElementById(inputId)
  if (inputEl) {
    const rect = inputEl.getBoundingClientRect()
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    
    dateSelectorTop.value = rect.bottom + scrollTop
    dateSelectorLeft.value = rect.left + scrollLeft
    dateSelectorVisible.value = true
  }
}

const getSelectedDate = () => {
  if (currentSelectingDateInput.value === 'single.date') return single.value.date
  if (currentSelectingDateInput.value === 'round.goDate') return round.value.goDate
  if (currentSelectingDateInput.value === 'round.backDate') return round.value.backDate
  return ''
}

const handleDateSelectorSelect = (dateStr) => {
  if (currentSelectingDateInput.value === 'single.date') {
    single.value.date = dateStr
  } else if (currentSelectingDateInput.value === 'round.goDate') {
    round.value.goDate = dateStr
    if (dayjs(round.value.backDate).isBefore(dayjs(dateStr))) {
      round.value.backDate = dateStr
    }
  } else if (currentSelectingDateInput.value === 'round.backDate') {
    round.value.backDate = dateStr
  }
  closeDateSelector()
}

const closeDateSelector = () => {
  dateSelectorVisible.value = false
}

onMounted(() => {
  document.addEventListener('click', handleGlobalClick)
})

onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick)
})
</script>

<!-- 引入原站样式与图标字体，确保外观一致性 -->
<style>
@import url('https://www.12306.cn/index/css/index_y_v50003.css');
/* 使用本地化的 12306 图标，实现稳定显示 */
@import url('@/styles/iconfont-12306-local.css');
/* 引入官网 iconfont 本地副本，确保 search-index 图标与官网一致 */
@import url('../assets/12306-icons/fonts/iconfont.css');

/* 在 search-index 内禁用本地 SVG mask，改用官网字体图标 */
.search-index .icon {
  background: none !important;
  -webkit-mask: none !important;
  mask: none !important;
}

/* 对齐搜索标签栏中的图标与文字 */
.search-index .search-tab-hd a {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  line-height: 1; /* 取消大行高，使用居中对齐 */
}
.search-index .search-tab-hd a .icon {
  display: inline-block;
  line-height: 1;
  vertical-align: middle;
  font-size: 16px; /* 与文字大小匹配，防止上下偏移 */
}

/* 让该模块成为定位上下文，承载查询框的绝对定位 */
.section-first {
  position: relative;
}

/* 局部容器居中偏移的复刻（原站通过 left:50% + margin-left 控制） */
.search-index {
  position: absolute;
  top: 50px;
  left: 50%;
  margin-left: -595px;
  width: 510px;
  z-index: 100;
  background: #fff;
  box-shadow: none;
}

/* 适配我们页面的宽度，保证轮播背景铺满 */
.fullSlide .bd li {
  background-size: cover;
}

/* 修复：官网样式将 .search-tab-item 默认隐藏，这里为激活项显示 */
.search-index .search-tab-bd .search-tab-item.active {
  display: block !important;
}

/* 固定轮播容器宽度为 1462，覆盖官网样式中的强制宽度 */
.fullSlide .bd {
  width: 1462px !important;
  max-width: 1462px !important;
  min-width: 1462px !important;
}

/* 让轮播容器在父级居中，对齐官网视觉 */
.fullSlide {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* 防止页面出现水平滚动条影响居中感知 */
.railway-homepage {
  overflow-x: hidden;
}
</style>

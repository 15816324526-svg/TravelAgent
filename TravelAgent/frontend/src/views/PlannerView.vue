
<script setup lang="ts">
import { computed , ref , onBeforeUnmount } from 'vue'
import { 
  submitPlanRequest , 
  subscribeToPlanTask 
} from '../api/planApi'
import type { 
  PlanRequest ,
  PlanResultSummary,
  PlanStageId,
  PlanTaskEvent
} from '../types/plan'
import { useRouter } from 'vue-router'
const router = useRouter()

function viewResult() {
  if (
    planningStatus.value !== 'completed' ||
    resultId.value === ''
  ) {
    return
  }

  router.push ({
    name: 'result',
    params: {
      resultId: resultId.value
    }
  })
}

import {
  MapPin,
  CalendarDays,
  ArrowRight,
  Calendar,

  BusFront,
   Footprints,
  CarTaxiFront,
  TrainFrontTunnel,
  CarFront,
  Bike,

  BuildingComplex,
  Hotel,
  BedSingle,

  Check,
  Sparkle
} from '@lucide/vue'

type PlanningStatus = 
  | 'idle'
  | 'submitting'
  | 'planning'
  | 'completed'
  | 'failed'

type PlanStageItem = {
  id: PlanStageId
  title: string
  description: string
}

type StageDisplayStatus = 
  | 'completed'
  | 'active'
  | 'pending'

type CalendarDay = {
  dateKey: string
  dayNumber: number
  isCurrentMonth: boolean
  isPast: boolean
}

const pageTitle = '智能旅行助手'
const pageSubtitle = '告诉我你的偏好，把沿途的美好安排妥当 喵~ '

function formatLocalDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const today = new Date()
const todayDate = formatLocalDate(today)

const stageLabels: Record<PlanStageId,string> = {
  understand_preferences: '正在理解你的旅行偏好',
  select_places_and_stay: '正在筛选景点与住宿区域',
  optimize_route: '正在优化路线与交通衔接',
  build_itinerary: '正在整理专属行程'
}

const stageItems: PlanStageItem[] = [
  {
    id: 'understand_preferences',
    title: '理解你的旅行偏好',
    description: '分析目的地、日期与旅行偏好'
  },
  {
    id: 'select_places_and_stay',
    title: '筛选景点与住宿区域',
    description: '选择合适的游览与住宿范围'
  },
  {
    id: 'optimize_route',
    title: '优化路线与交通衔接',
    description: '平衡浏览顺序与交通时间'
  },
  {
    id: 'build_itinerary',
    title: '整理专属行程',
    description: '汇总每日安排与出行提示'
  }
]

const destination = ref('杭州，浙江')
const startDate = ref('2026-11-14')
const endDate = ref('2026-11-15')

const initialVisibleDate =
  startDate.value !== ''
    ? new Date(`${startDate.value}T00:00:00`)
    : today

const visibleYear = ref(initialVisibleDate.getFullYear())
const visibleMonth = ref(initialVisibleDate.getMonth())
const weekdayLabels = ['一','二','三','四','五','六','日']

const calendarDays = computed<CalendarDay[]>(() => {
  const firstDay = new Date(
    visibleYear.value,
    visibleMonth.value,
    1
  )

  const mondayOffset = (firstDay.getDay() + 6) % 7

  const gridStart = new Date(
    visibleYear.value,
    visibleMonth.value,
    1 - mondayOffset
  )

  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(gridStart)

    date.setDate(gridStart.getDate() + index)

    const dateKey = formatLocalDate(date)

    return {
      dateKey,
      dayNumber: date.getDate(),

      isCurrentMonth:
        date.getFullYear() === visibleYear.value &&
        date.getMonth() === visibleMonth.value,

      isPast: dateKey < todayDate
    }
  })
})

const calendarTitle = computed(() => {
  return `${visibleYear.value}年 ${visibleMonth.value + 1}月`
})

const canGoToPreviousMonth = computed(() => {
  const currentYear = today.getFullYear()
  const currentMonth = today.getMonth()

  return (
    visibleYear.value > currentYear ||
    (
      visibleYear.value === currentYear &&
      visibleMonth.value > currentMonth
    )
  )
})

const calendarSelectionText = computed(() => {
  if (
    startDate.value !== '' &&
    endDate.value !== ''
  ) {
    return (
      `${formatCalendarDate(startDate.value)}` +
      ` — ${formatCalendarDate(endDate.value)}`
    )
  }

  if (startDate.value !== '') {
    return `${formatCalendarDate(startDate.value)}，请选择另一个日期`
  }

  return '请选择出发日期'
})

function goToPreviousMonth() {
  if (!canGoToPreviousMonth.value) {
    return
  }

  if (visibleMonth.value === 0) {
    visibleYear.value -= 1
    visibleMonth.value = 11
    return
  }

  visibleMonth.value -= 1
}

function goToNextMonth() {
  if (visibleMonth.value === 11) {
    visibleYear.value += 1
    visibleMonth.value = 0
    return
  }

  visibleMonth.value += 1
}

function isCalendarDayDisabled(day: CalendarDay): boolean {
  if (day.isPast) {
    return true
  }

  const hasCompleteRange =
    startDate.value !== '' &&
    endDate.value !== ''

  if (!hasCompleteRange) {
    return false
  }

  return (
    day.dateKey !== startDate.value &&
    day.dateKey !== endDate.value
  )
}

function isDateInSelectedRange(dateKey: string): boolean {
  if (
    startDate.value === '' ||
    endDate.value === ''
  ) {
    return false
  }

  return (
    dateKey > startDate.value &&
    dateKey < endDate.value
  )
}

function selectCalendarDate(dateKey: string) {
  if (dateKey < todayDate) {
    return
  }

  /*
   * 如果用户手动清空了开始日期，
   * 但结束日期还有值，就把剩下的日期整理到 startDate。
   */
  if (
    startDate.value === '' &&
    endDate.value !== ''
  ) {
    startDate.value = endDate.value
    endDate.value = ''
  }

  /* 当前没有选择任何日期 */
  if (
    startDate.value === '' &&
    endDate.value === ''
  ) {
    startDate.value = dateKey
    showCalendarMonth(dateKey)
    return
  }

  /* 当前只有一个日期 */
  if (
    startDate.value !== '' &&
    endDate.value === ''
  ) {
    if (dateKey < startDate.value) {
      endDate.value = startDate.value
      startDate.value = dateKey
    } else {
      endDate.value = dateKey
    }

    showCalendarMonth(dateKey)
    return
  }

  /*
   * 开始和结束是同一天：
   * 再点击一次就取消整个选择。
   */
  if (
    startDate.value === endDate.value &&
    dateKey === startDate.value
  ) {
    startDate.value = ''
    endDate.value = ''
    return
  }

  /* 点击开始端点：留下原来的结束日期 */
  if (dateKey === startDate.value) {
    startDate.value = endDate.value
    endDate.value = ''
    return
  }

  /* 点击结束端点：留下原来的开始日期 */
  if (dateKey === endDate.value) {
    endDate.value = ''
  }
}

function showCalendarMonth(dateKey: string) {
  const date = new Date(`${dateKey}T00:00:00`)

  visibleYear.value = date.getFullYear()
  visibleMonth.value = date.getMonth()
}

function handleStartDateChange() {
  if (
    startDate.value !== '' &&
    startDate.value >= todayDate
  ) {
    showCalendarMonth(startDate.value)
    return
  }

  /*
   * 用户清空开始日期，但结束日期仍然存在：
   * 把唯一剩下的日期整理到 startDate。
   */
  if (
    startDate.value === '' &&
    endDate.value !== ''
  ) {
    startDate.value = endDate.value
    endDate.value = ''

    showCalendarMonth(startDate.value)
  }
}

function handleEndDateChange() {
  if (
    endDate.value !== '' &&
    endDate.value >= todayDate
  ) {
    showCalendarMonth(endDate.value)
  }
}

function formatCalendarDate(dateKey: string): string {
  if (dateKey === '') {
    return ''
  }

  const [, month, day] = dateKey.split('-')

  return `${Number(month)}月${Number(day)}日`
}

const transportOptions = [
  {
    label:'公共交通',
    icon:BusFront
  },
  {label:'步行',
    icon:Footprints
  },
  {
    label:'出租车',
    icon:CarTaxiFront
  },
  {
    label:'地铁',
    icon:TrainFrontTunnel
  },
  {
    label:'自驾',
    icon:CarFront
  },
  {
    label:'骑行',
    icon:Bike
  }
]
const selectedTransports = ref<string[]>([])

const accommodationOptions = [
  {
    label:'公寓',
    icon:BuildingComplex
  },
  {
    label:'酒店',
    icon:Hotel
  },
  {
    label:'青旅',
    icon:BedSingle
  }
]
const selectedAccommodations = ref<string[]>([])

const accommodationBudget = ref<number | ''>(500)
const travelNumber = ref<number>(10)
const millisecondsPerDay = 1000 * 60 * 60 * 24

const specialRequirements = ref('')
const maxRequirementsLength = 2000

const submittedRequest = ref<PlanRequest | null>(null)

const planningStatus = ref<PlanningStatus>('idle')

const taskId = ref('')
const progress = ref(0)
const currentStage = ref<PlanStageId | null>(null)
const etaSeconds = ref<number | null>(null)

const resultId = ref('')
const resultSummary = ref<PlanResultSummary | null>(null)


const submitError = ref('')

let unsubscribePlanTask: (() => void) | null = null

const isSubmitting = computed(() => {
  return planningStatus.value === 'submitting'
})

const isPlanningActive = computed(() => {
  return (
    planningStatus.value === 'submitting' ||
    planningStatus.value === 'planning'
  )
})

const currentStep = computed<1 | 2 | 3>(() => {
  if (planningStatus.value === `completed`) {
    return 3
  }

  if (
    planningStatus.value === `submitting` ||
    planningStatus.value === 'planning' ||
    planningStatus.value === 'failed'
  ) {
    return 2
  }

  return 1
})

const progressText = computed(() => {
  if (planningStatus.value === 'idle') {
    return '等待开始'
  }

  if (planningStatus.value === 'submitting') {
    return '正在创建规划任务'
  }

  if (
    planningStatus.value === 'planning' &&
    currentStage.value !== null
  ) {
    return stageLabels[currentStage.value]
  }

  if (planningStatus.value === 'completed') {
    return '全部规划已完成'
  }

  if (planningStatus.value === 'failed') {
    return '规划失败'
  }

  return '等待开始'
})

const planningOverviewTitle = computed(() => {
  if (planningStatus.value === 'idle') {
    return '等待开始规划'
  }

  if (planningStatus.value === 'submitting') {
    return '正在准备你的旅程'
  }

  if (planningStatus.value === 'planning') {
    return '正在准备你的旅程'
  }

  if (planningStatus.value === 'completed') {
    return '旅程规划已完成'
  }

  if (planningStatus.value === 'failed') {
    return '规划暂时失败'
  }
  
  return '等待开始规划'
})

function getStageStatus(
  stageId: PlanStageId
): StageDisplayStatus {
  if (planningStatus.value === 'completed') {
    return 'completed'
  }

  if (currentStage.value === null) {
    return 'pending'
  }

  const currentStageIndex = stageItems.findIndex(
    stage => stage.id === currentStage.value
  )

  const stageIndex = stageItems.findIndex(
    stage => stage.id === stageId
  )

  if (
    currentStageIndex === -1 ||
    stageIndex === -1
  ) {
    return 'pending'
  }

  if (stageIndex < currentStageIndex) {
    return 'completed'
  }

  if (
    stageIndex === currentStageIndex &&
    planningStatus.value === 'planning'
  ) {
    return 'active'
  }

  return 'pending'
}

const dateError = computed(() => {
  if (
    (startDate.value !== '' && startDate.value < todayDate ) ||
    (endDate.value !== '' && endDate.value < todayDate)
  ) {
    return '不能选择今天以前的日期'
  }

  if (startDate.value === '' || endDate.value === '') {
    return ''
  }

  if (endDate.value < startDate.value) {
    return '结束时间不能早于开始时间'
  }

  return ''
})
const budgetError = computed(() => {
  if (accommodationBudget.value === ''){
    return '请输入每晚居住预算'
  }

  if (accommodationBudget.value < 0) {
    return '居住预算不能小于 0 '
  }

  return ''
})
const numberError = computed(() => {
  if(travelNumber.value === 0){
    return '请输入出行人数'
  }

  if(travelNumber.value < 0){
    return '人数不能少于 0 '
  }
})
const requirementsLength = computed(() => {
  return specialRequirements.value.length
})
const tripDuration = computed(() => {
  if (startDate.value === '' || endDate.value === '' || dateError.value !== ''){
    return ''
  }

  const start = new Date(startDate.value)
  const end = new Date(endDate.value)

  const nights = Math.round(
    (end.getTime() - start.getTime()) / millisecondsPerDay
  )

  const days = nights + 1

  return `共 ${days} 天 · ${nights} 晚`
})
const isFormValid = computed(() => {
  return (
    destination.value.trim() !=='' &&
    startDate.value !=='' &&
    endDate.value !== '' &&
    dateError.value === '' &&
    accommodationBudget.value !== '' &&
    budgetError.value === '' &&
    selectedTransports.value.length > 0 &&
    selectedAccommodations.value.length > 0 &&
    requirementsLength.value <= maxRequirementsLength
  )
})

function toggleTransport(transport:string) {
  const selectedIndex = selectedTransports.value.indexOf(transport)

  if (selectedIndex === -1) {
    selectedTransports.value.push(transport)
    return
  }

  selectedTransports.value.splice(selectedIndex,1)
}

function toggleAccommodation(accommodation:string) {
  const selectedIndex = selectedAccommodations.value.indexOf(accommodation)
  
  if (selectedIndex === -1) {
    selectedAccommodations.value.push(accommodation)
    return
  }

  selectedAccommodations.value.splice(selectedIndex,1)
}

function createPlanRequest(): PlanRequest | null {
  if (!isFormValid.value || accommodationBudget.value === '') {
    return null
  }

  return {
    destination: destination.value.trim(),
    start_date: startDate.value,
    end_date: endDate.value,
    transport_modes: [...selectedTransports.value],
    accommodation_types: [...selectedAccommodations.value],
    budget_per_night: accommodationBudget.value,
    special_requirements: specialRequirements.value.trim(),
    traveler_account:travelNumber.value
  }
}

async function submitPlan() {
  const request = createPlanRequest()

  if (request === null) {
    return
  }

  stopPlanSubscription()

  planningStatus.value = 'submitting'
  submitError.value = ''
  submittedRequest.value = null

  taskId.value = ''
  progress.value = 0
  currentStage.value = null
  etaSeconds.value = null
  resultId.value = ''
  resultSummary.value = null

  try {
    const accepted = await submitPlanRequest(request)

    taskId.value = accepted.task_id
    submittedRequest.value = request
    planningStatus.value = 'planning'

    unsubscribePlanTask = subscribeToPlanTask(
      accepted.task_id,
      handlePlanEvent
    )
  } catch (error) {
    planningStatus.value = 'failed'

    submitError.value =
      error instanceof Error
        ? error.message
        : '创建规划任务失败，请稍后重试'
  }
}

function stopPlanSubscription() {
  if (unsubscribePlanTask !== null) {
    unsubscribePlanTask()
    unsubscribePlanTask = null
  }
}

//任务处理
function handlePlanEvent(event: PlanTaskEvent) {
  if (event.task_id !== taskId.value){
    return 
  }

  if (event.type === 'progress') {
    planningStatus.value = 'planning'
    progress.value = event.progress
    currentStage.value = event.current_stage
    etaSeconds.value = event.eta_seconds
    return
  }

  if (event.type === 'completed') {
    planningStatus.value = 'completed'
    progress.value = event.progress
    currentStage.value = null
    etaSeconds.value = null
    resultId.value = event.result_id
    resultSummary.value = event.summary

    stopPlanSubscription()
    return
  }

  planningStatus.value = 'failed'
  etaSeconds.value = null
  submitError.value = event.message

  stopPlanSubscription()
}

onBeforeUnmount(() => {
  stopPlanSubscription()
})

</script>

<template>
  <main class="planner-page">    

    <div class="page-top">
      <div class="page-heading">
        <h1>{{ pageTitle }}</h1>
        <p>{{ pageSubtitle }}</p>
      </div>

      <nav class="page-stepper" aria-label="规划步骤">
        <ol class="step-list">
          <li class="step-item"
              :class="{ 
                'is-active': currentStep === 1 ,
                'is-completed': currentStep > 0
              }">
            <span class="step-number">1</span>
            <span> 填写偏好 </span>
          </li>
          <li class="step-item"
              :class="{ 
                'is-active': currentStep === 2 ,
                'is-completed': currentStep > 1
              }">
            <span class="step-number">2</span>
            <span> 智能规划 </span>
          </li>
          <li class="step-item"
              :class="{ 
                'is-active': currentStep === 3,
                'is-completed': currentStep > 2
              }"
            >
            <span class="step-number">3</span>
            <span> 查看行程 </span>
          </li>
        </ol>
      </nav>
    </div>

  <div class="planner-layout">
    <section class="preference-card">
      <h2>这次，想去哪里 喵 ~ ( > 3 < )</h2>
      <form class="preference-form" @submit.prevent="submitPlan">
        <div class="form-field">    
          <label for="destination">目的城市 ʕ•ᴥ•ʔ</label>
          <div class="input-with-icon">
            <MapPin
              class="field-icon"
              :size="20"
              :stroke-width="1.8"
              aria-hidden="true"
            />

            <input 
            v-model="destination"
            class="form-input"          
            id="destination"         
            name="destination"
            type="text"
            placeholder="请输入目的城市"
          />
          </div>
        </div>

        <div class="date-fields">
          <div class="form-field">
            <label for="start-date">开始时间 ~ (≧▽≦) ~ </label>
            <div class="input-with-icon">
              <Calendar
                class="field-icon"
                :size="20"
                :stroke-width="1.8"
                aria-hidden="true"
              />

              <input
                v-model="startDate"
                class="form-input"
                id="start-date"
                name="startDate"
                type="date"
                :min="todayDate" 
                @change="handleStartDateChange"
              />
            </div>
          </div>

          <div class="form-field">
            <label for="end-date">结束时间 ~ (^_^) ~ </label>
            <div class="input-with-icon">
              <Calendar
                class="field-icon"
                :size="20"
                :stroke-width="1.8"
                aria-hidden="true"
              />
              <input
                v-model="endDate"
                class="form-input"
                id="end-date"
                name="endDate"
                :min="startDate || todayDate"
                type="date"
                @change="handleEndDateChange"
              />
            </div>
          </div>
        </div>

        <p v-if="tripDuration">
          {{ tripDuration }}
        </p>

        <p v-if="dateError" class="form-error">
          {{ dateError }}
        </p>

        <fieldset class="choice-fieldset">
          <legend>
            交通方式
            <span class="required-hint">至少选择一项 · 可多选</span>
          </legend>
          <div class="choice-options">

            <button 
            v-for="transport in transportOptions"
            :key="transport.label"
            type="button" 
            class="choice-option"
            :class="{ 'is-selected': selectedTransports.includes(transport.label) }"
            :aria-pressed="selectedTransports.includes(transport.label)"
            @click="toggleTransport(transport.label)"
            >
            <component
              :is="transport.icon"
              :size="18"
              :stroke-width="1.8"
              aria-hidden="true"
              />

            <span>{{ transport.label }}</span>

            <Check
              v-if="selectedTransports.includes(transport.label)"
              class="choicce-check"
              :size="16"
              aria-hidden="true"
            />
            </button>
          </div>
        </fieldset>

        <fieldset class="choice-fieldset">
          <legend>
            居住方式
            <span class="required-hint">至少选择一项 · 可多选</span>
          </legend>
          <div class="choice-options">

            <button 
            v-for="accommodation in accommodationOptions"
            :key="accommodation.label"
            type="button" 
            class="choice-option"
            :class="{ 'is-selected': selectedAccommodations.includes(accommodation.label) }"
            :aria-pressed="selectedAccommodations.includes(accommodation.label)"
            @click="toggleAccommodation(accommodation.label)"
            >
            <component
              :is="accommodation.icon"
              :size="18"
              :stroke-width="1.8"
              aria-hidden="true"
            />
            <span>{{ accommodation.label }}</span>

            <Check
              v-if="selectedTransports.includes(accommodation.label)"
              class="choice-check"
              :size="18"
              aria-hidden="true"
            />
            </button>

          </div>
        </fieldset>

        <div class="second-field">
          <div class="budget-field">
          <label for="accommodation-budget">居住预算</label>

          <div
            class="budget-control"
            :class="{ 'has-error': budgetError !== '' }"
            >
            <span aria-hidden="true">￥</span>

            <input
              v-model.number="accommodationBudget"
              id="accommodation-budget"
              name="accommodationBudget"
              type="number"
              min="0"
              step="50"
              :aria-invalid="budgetError !== ''"
              />

              <span class="budget-unit">元 / 晚</span>
          </div>

          <p v-if="budgetError" class="form-error">
            {{ budgetError }}
          </p>
          </div>

          <div class="travel-number">
          <label for="travel-total-number">出行人数</label>

          <div
            class="travel-control"
            >
            <span aria-hidden="true">☃</span>

            <input
              v-model.number="travelNumber"
              id="travel-total-number"
              name="travel-number"
              type="number"
              min="1"
              />

              <span class="number-unit">人</span>

              <p v-if="numberError" class="form-error">
              {{ numberError }}
              </p>
          </div>
          </div>
        </div>

        <div class="requirements-field">
          <div class="field-heading">
            <label for="special-requirements">额外要求 ~ (˶˃ ᵕ ˂˶)</label>
            <span class="field-hint">选填 ~ 让安排更懂你 (˶ᵔ ᵕ ᵔ˶) </span>
          </div>

          <div class="textarea-control">
            <textarea
              v-model="specialRequirements"
              id="special-requirements"
              name="specialRequirements"
              :maxlength="maxRequirementsLength"
              placeholder="例如:喜欢自然风景和当地小吃 (*^▽^*) ，不要安排太赶…… o(╥﹏╥)o "
              ></textarea>

              <div class="textarea-footer">
                <span>饮食偏好、同行人、无障碍需求，都可以写在这里喵 ~ ( ˶ˆᗜˆ˵ ) </span>

                <span 
                  class="character-count"
                  :class="{ 'is-near-limit':requirementsLength >= 1800 }"
                >
                  {{ requirementsLength }} / {{ maxRequirementsLength }}
                </span>
              </div>
          </div>

        </div>

        <div
        class="work-progress"
        aria-live="polite"
      >
        <div class="progress-heading">
          <span>
            工作进度 ~ {{ progressText }}
          </span>

          <strong>{{ progress }}%</strong>
        </div>

        <div
          class="progress-track"
          role = "progressbar"
          aria-label="智能规划进度"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          <div
            class="progress-fill"
            :style="{ width: `${progress}%`}"
          ></div>
        </div>

       <p
          v-if="
            planningStatus === 'planning' &&
            etaSeconds !== null
          "

          class="progress-estimate"
        >
          预计还需约 {{ etaSeconds }} 秒，请稍候
        </p>
      </div>

        <button 
          :type="
            planningStatus === 'completed'
              ? 'button'
              : 'submit'
          "
          class="submit-button"
          :class="{
            'is-result-button': planningStatus === 'completed'
          }"
          @click="
            planningStatus === 'completed' && viewResult()"
          :disabled="
            planningStatus === 'completed'
              ?resultId === ''
              : !isFormValid || isPlanningActive
          "
          :aria-busy="isPlanningActive"
        >


        <span v-if="planningStatus === 'submitting'">正在创建规划任务，请稍等…… °‧ 𓆝 𓆟 𓆞 ·｡ </span>
        <span v-else-if="planningStatus === 'planning'">正在智能规划，{{ progress }}% °‧ 𓆝 𓆟 𓆞 ·｡ </span>
        <span 
          v-else-if="planningStatus === 'completed'"
          class="button-content"
          >
           <span>规划已完成 (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ,点击查看规划行程 </span>    

           <ArrowRight
             class="button-arrow"
             :size="14"
             :stroke-width="5"
             aria-hidden="true"
            />
          
        </span>
        <span v-else> ٩(◕‿◕｡)۶ ~开始智能规划~ ٩(●˙▿˙●)۶ </span>
        </button>

        <p
          v-if="submitError"
          class="form-error"
          role="alert"
          >{{ submitError }}
        </p>
      </form>

      <div
        class="work-progress"
        aria-live="polite"
      >
        <div class="progress-heading">
          <span>
            工作进度 ~ {{ progressText }}
          </span>

          <strong>{{ progress }}%</strong>
        </div>

        <div
          class="progress-track"
          role = "progressbar"
          aria-label="智能规划进度"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          <div
            class="progress-fill"
            :style="{ width: `${progress}%`}"
          ></div>
        </div>

       <p
          v-if="
            planningStatus === 'planning' &&
            etaSeconds !== null
          "

          class="progress-estimate"
        >
          预计还需约 {{ etaSeconds }} 秒，请稍候
        </p>
      </div>

      
    </section>
    
    <aside class="side-column">
      <section class="calendar-card">
        <div class="calendar-card-heading">
          <h2>出行日历</h2>
          <span>日期选择器</span>
        </div>

        <div class="calendar-navigation">
          <button 
            type="button"
            class="calendar-nav-button"
            :disabled="!canGoToPreviousMonth"
            aria-label="查看上个月"
            @click="goToPreviousMonth"
          >
            ‹
          </button>

          <strong>{{ calendarTitle }}</strong>

          <button
            type="button"
            class="calendar-nav-button"
            aria-label="查看下个月"
            @click="goToNextMonth"
          >
            ›
          </button>
        </div>

        <div class="calendar-weekdays">
          <span
            v-for="weekday in weekdayLabels"
            :key="weekday"
          >
            {{ weekday }}
          </span>
        </div>

        <div class="calendar-grid">
          <button
            v-for="day in calendarDays"
            :key="day.dateKey"
            type="button"
            class="calendar-day"
            :class="{
              'is-outside-month': !day.isCurrentMonth,
              'is-today': day.dateKey === todayDate,
              'is-in-range': isDateInSelectedRange(day.dateKey),

              'is-range-start':
                startDate !== '' &&
                endDate !== '' &&
                startDate !== endDate &&
                day.dateKey === startDate,
              
              'is-range-end': 
                startDate !== '' &&
                endDate !== '' &&
                startDate !== endDate &&
                day.dateKey === endDate,

              'is-selected':
                day.dateKey === startDate ||
                day.dateKey === endDate
            }"
            :disabled="isCalendarDayDisabled(day)"
            :aria-label="day.dateKey"
            :aria-pressed="
              day.dateKey === startDate ||
              day.dateKey === endDate
            "
            @click="selectCalendarDate(day.dateKey)"
            >
              {{ day.dayNumber }}
          </button>
      </div>

        <div class="calendar-summary">
          <div class="calendar-summary-copy">
            <span>日期选择</span>
            <strong>{{ calendarSelectionText }}</strong>
          </div>

          <span
            v-if="tripDuration"
            class="calendar-duration"
          >
            {{ tripDuration }}
          </span>
        </div>
      </section>

      <section class="planning-card">
      <template
        v-if="
          planningStatus === 'completed' &&
          resultSummary !== null
          "
      >
        <div class="completion-summary">
          <div
            class="completion-check"
            aria-hidden="true"
          >
            ✓
          </div>

          <h2>已经为你安排妥当</h2>

        <p>
          完整行程已经生成，可以查看规划结果。
        </p>

        <div class="completion-stats">
          <div class="completion-stat">
            <strong>
              {{ resultSummary.days }}天{{ resultSummary.nights }}晚
            </strong>
            <span>行程时长</span>
          </div>

          <div class="completion-stat">
            <strong>
              {{ resultSummary.place_count }}处
            </strong>
            <span>精选地点</span>
          </div>

          <div class="completion-stat">
            <strong>
              ≤{{ resultSummary.budget_per_night }}元
            </strong>
            <span>每晚住宿</span>
          </div>

        </div>

        <ul
          v-if="resultSummary.highlights.length > 0"
          class="completion-highlights"
        >
          <li
            v-for="(highlight, index) in resultSummary.highlights"
            :key="`${index}-${highlight}`"
            class="completion-highlight"
          >
            <span 
              class="highlight-check"
              aria-hidden="true"
            >
              ✓
            </span>

            <span>{{ highlight }}</span>
          </li>
        </ul>
      </div>
    </template>
    <template v-else>

      <div class="planning-overview">
      <div
        class="circular-progress"
        role="progressbar"
        aria-label="右侧智能规划进度"
        :aria-valuenow="progress"
        aria-valuemin="0"
        aria-valuemax="100"
        :style="{
          background: `conic-gradient(#708278 0% ${progress}%,#e5e8e3 ${progress}% 100%)`
        }"
      >
        <span>{{ progress }}%</span>
      </div>

      <div class="planning-overview-copy">
        <h3>{{ planningOverviewTitle }}</h3>

        <p
          v-if="
            planningStatus === 'planning' &&
            etaSeconds !== null
          "
        >
          预计还需约 {{ etaSeconds }} 秒
        </p>

        <p v-else>
          {{ progressText }}
        </p>
      </div>
      </div>

      <ol class="stage-list">
        <li
          v-for="stage in stageItems"
          :key="stage.id"
          class="stage-item"
          :class="`is-${getStageStatus(stage.id)}`"
        >

          <span 
            class="stage-marker"
            aria-hidden="true"
          >
            <span
              v-if="
                getStageStatus(stage.id) === 'completed'
              "
            >
              √
            </span>

            <span
              v-else-if="
                getStageStatus(stage.id) === 'active'
              "
            >
             ↻
            </span>
          </span>
          
        <div class="stage-copy">
          <h3>{{ stage.title }}</h3>
          <p>{{ stage.description }}</p>
        </div>
        </li>
      </ol>
    </template>
      </section>
    </aside>
  </div>
  </main>
</template>

<style scoped>
.input-with-icon {
  position: relative;
}

.field-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #7d847e;
  pointer-events: none;
}

.input-with-icon .form-input {
  padding-left: 48px;
}

.page-top {
  display: flex;
  justify-content: space-between;/*justify-content: space-between：第一个孩子靠左，最后一个孩子靠右，中间空间自动分配*/
  gap: 32px;/*窗口变窄时，保证两边至少留有 32px，不是强行隔开 800px。*/
  align-items: flex-start;/*标题和步骤条都从顶部对齐*/
}

.page-heading h1{
  margin: 0; /*h1 p 浏览器会自动加外边距 可以自己控制*/
}

.page-heading p{
  margin: 8px 0 0;
  color: #7d847e;
}

.step-list {
  display: flex;          /* 开启 Flexbox */
  align-items: center;    /* 三个步骤在垂直方向居中 */
  gap: 0;                 /* 步骤距离交给连接线的 margin 控制 */
  margin: 0;              /* 清除 ol 自带的外边距 */
  padding: 0;             /* 清除 ol 自带的左侧内边距 */
  list-style: none;       /* 清除 ol 自动生成的编号 */
  font-size: 16px;        /* 设置步骤文字大小 */
}

/* 单独一个步骤：包含圆圈、文字和后面的连接线 */
.step-item {
  display: flex;          /* 让圆圈、文字和连接线横向排列 */
  align-items: center;    /* 让圆圈和文字处在同一水平线上 */
  color: #8a908b;         /* 未激活步骤的文字颜色 */
  white-space: nowrap;    /* 不允许“填写偏好”中途换行 */
}

/* 每个步骤前面的圆形编号 */
.step-number {
  width: 28px;            /* 圆圈宽度 */
  height: 28px;           /* 圆圈高度；与宽度相同才能成为正圆 */
  display: grid;          /* 使用 Grid 布局数字 */
  place-items: center;    /* 让数字水平、垂直同时居中 */
  margin-right: 8px;      /* 圆圈与右侧文字的距离 */
  border-radius: 50%;     /* 把正方形变成圆形 */
  background-color: #c7d4ba; /* 普通圆圈的底色 */
  color: #556057;         /* 圆圈内部数字的颜色 */
  font-size: 13px;        /* 数字大小 */
  flex-shrink: 0;         /* 空间不足时不允许圆圈被压扁 */

  transition:
    background-color 200ms ease; /* 圆圈底色变化时增加过渡动画 */
}

/* 当前步骤的文字 */
.step-item.is-active {
  color: #303530;         /* 当前步骤文字颜色加深 */
  font-weight: 600;       /* 当前步骤文字加粗 */
}

/* 当前步骤圆圈的底色，只改变圆圈面积 */
.step-item.is-active .step-number {
  background-color: #60826a;
  color: #ffffff
}

/* 给除最后一步以外的步骤添加连接线 */
.step-item:not(:last-child)::after {
  content: '';            /* 创建一个空的虚拟元素 */
  width: 40px;            /* 连接线长度 */
  height: 1px;            /* 连接线粗细 */
  margin: 0 16px;         /* 连接线左右留白 */
  background-color: #e1e4de; /* 连接线颜色 */
}

/* 已经经过的步骤文字 */
.step-item.is-completed {
  color: #52675a;
  font-weight: 600;
}

/* 已经经过的步骤圆圈面积变为深绿色 */
.step-item.is-completed .step-number {
  background-color: #708278;
  color: #ffffff;
}

/* 已完成步骤后面的连接线也变深 */
.step-item.is-completed::after {
  background-color: #708278;
}

.side-column {
  display: flex;          /* 开启 Flexbox */
  flex-direction: column; /* 日历和规划卡片上下排列 */
  gap: 24px;              /* 两张卡片之间的距离 */
  min-width: 0;           /* 允许右栏在空间不足时缩小 */
}

.calendar-card {
  padding: 28px;                 /* 内容与卡片边缘的距离 */
  border: 1px solid #e1e4de;     /* 卡片边框 */
  border-radius: 20px;            /* 卡片圆角 */
  background-color: #ffffff;      /* 卡片底色 */
}

.calendar-card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.calendar-card-heading h2 {
  margin: 0;
  font-size: 18px;
}

.calendar-card-heading span {
  color: #8a908b;
  font-size: 13px;
}

.calendar-navigation {
  display: grid;
  grid-template-columns: 40px 1fr 40px;
  align-items: center;
  margin-top: 24px;
}

.calendar-nav-button {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  padding: 0;
  border: 0;
  border-radius: 10px;
  background-color: transparent;
  color: #65716a;
  font-size: 26px;
  cursor: pointer;
}

.calendar-nav-button:hover {
  background-color: #f0f2ee;
}

.calendar-nav-button:disabled {
  color: #c5cac6;
  cursor: not-allowed;
}

/* 星期标题和日期区域都平均分成七列 */
.calendar-weekdays,
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  /*repeat(7, ...)：重复七次，也就是七列。1fr：每列取得相同的一份空间。minmax(0, 1fr)：空间不足时允许缩小，不被内容撑破。*/
}

.calendar-weekdays {
  margin-top: 20px;
  color: #8a908b;
  font-size: 12px;
  text-align: center;
}

.calendar-grid {
  column-gap: 0;  /* 同一行日期不留空，让范围背景连接 */
  row-gap: 4px;   /* 不同星期行之间仍然保留距离 */
  margin-top: 8px;
}

.calendar-day {
  min-width: 0;
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  padding: 0;
  border: 0;
  border-radius: 10px;
  background-color: transparent;
  color: #303530;
  font: inherit;
  cursor: pointer;
}

.calendar-day:hover:not(:disabled) {
  background-color: #f0f2ee;
}

.calendar-day.is-outside-month {
  color: #adb3ae;
}

/* 开始和结束日期之间的日期 */
.calendar-day.is-in-range {
  border-radius: 0;
  background-color: #edf2ed;
  color: #52675a;
}

/* 范围日期虽然不能点击，但文字仍保持清晰 */
.calendar-day.is-in-range:disabled {
  color: #52675a;
}

.calendar-day.is-selected {
  background-color: #708278;
  color: #ffffff;
  font-weight: 600;
}

/* 范围开始端：左边圆、右边直 */
.calendar-day.is-range-start {
  border-radius: 10px 0 0 10px;
}

/* 范围结束端：左边直、右边圆 */
.calendar-day.is-range-end {
  border-radius: 0 10px 10px 0;
}

.calendar-day.is-selected:hover:not(:disabled) {
  background-color: #607269;
}

.calendar-day:disabled {
  color: #d1d5d1;
  cursor: not-allowed;
}

.calendar-summary {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e5e8e3;
}

.calendar-summary-copy {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.calendar-summary-copy span {
  color: #8a908b;
  font-size: 12px;
}

.calendar-summary-copy strong {
  color: #303530;
  font-size: 14px;
}

.calendar-duration {
  padding: 8px 12px;
  border-radius: 10px;
  background-color: #edf2ed;
  color: #52675a;
  font-size: 13px;
  white-space: nowrap;
}

.calendar-day.is-today:not(.is-selected) {
  box-shadow: inset 0 0 0 1px #9aac9f;
  font-weight: 600;
}

.calendar-day:focus-visible {
  z-index: 1;
  outline: 2px solid #708278;
  outline-offset: 2px;
}

.planner-page {       /*设置类名为planner-page的元素的样式，.找class*/
  max-width: 1440px;
  margin: 0 auto;
  padding: 24px;       /*元素内部留白宽度为24像素*/ 
}

.preference-card {
  /*margin-top: 32px; 元素外部的距离，上方32px*/
  padding: 24px;    /*元素边缘与内部内容之间的距离*/
  background-color: #ffffff;
  border: 1px solid #e1e4de; /*border元素边框：粗细 线条类型 颜色*/
  border-radius: 20px; /*圆角边界半径，pixel数值越大圆角越明显*/
}

/*
上面的副标题
      ↓
  32px margin       ← 卡片外部距离
┌─────────────────────┐
│    24px padding     │ ← 卡片内部距离
│    h2 标题          │
│    24px padding     │
└─────────────────────┘
  ┌─────────────────────────────┐
  │         margin（外边距）     │  ← 盒子和"别人"之间留的空
  │  ┌───────────────────────┐  │
  │  │  padding（内边距）     │  │  ← 盒子内壁到"内容"之间留的空
  │  │  ┌─────────────────┐  │  │
  │  │  │   内容（文字/图  │  │  │  ← 真正的内容
  │  │  └─────────────────┘  │  │
  │  └───────────────────────┘  │
  └─────────────────────────────┘
*/

.preference-form {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/*
原来可能是：

目的城市 [输入框]

设置 column 后：

目的城市
[输入框]
*/

.form-field {
  display: flex; /*block是站一整行接着竖着排 inline是排成一排 flex弹性盒子 */
  flex-direction: column; /*父元素有flex才生效 row和column */
  gap: 8px;                /*flex布局中子元素之间的间距*/
}

.form-input {
  width: 100%; /*px就是宽像素 %是父容器的百分比 auto自动决定默认值*/
  height: 52px;
  padding: 0 16px;  /*0→上方和下方内部留白 16px→左边和右边内部留白*/
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #f8f9f7;
}

.form-input:focus {/*.form-input→找到输入框 :focus→仅限它正在获得焦点的时候*/
  border-color: #708278;
  outline: 3px solid #dfe7e1; /*outline 是边框外面额外显示的一圈轮廓*/
}

.date-fields { /*之前的 Flexbox 更像是在一个方向上排列内容：横向，或者纵向*/
  display: grid;
  grid-template-columns: 1fr 1fr; /*fr是 fraction的缩写，表示“可用空间的一份”*/
  gap: 16px;
}

.second-field {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr; /*fr是 fraction的缩写，表示“可用空间的一份”*/
  gap: 16px;
}

.form-error {
  margin: 0;
  color: #b42318;
  font-size: 14px;
}

.choice-fieldset{
  margin: 0;/*margin是外边距 padding是内边距 */
  padding: 0;/*两个数就是上下 左右 四个数就是顺时针上右下左 */
  border: 0; /*padding-top就是只设上面 */
}

.choice-fieldset legend {
  margin-bottom: 12px;
  font-weight: 600;
}

.choice-options {
  display: flex;
  flex-wrap: wrap; /*nowrap wrap只控制是否换行 */
  gap: 12px;
  margin-left: 3px;
}

.choice-option {
  padding: 12px 18px;
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #ffffff;
  color: #303530;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.choice-option.is-selected {
  border-color: #b8c8bc;
  background-color: #edf2ed;
  color: #52675a;
}

.budget-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 360px;
}

.budget-control {
  height: 52px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #f8f9f7;
}

.budget-control:focus-within {
  border-color: #708278;
  outline: 3px solid #dfe7e1;
}

.budget-control.has-error {
  border-color: #b42318;
}

.budget-control input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  background-color :transparent;
  font: inherit;
}

.budget-unit {
  color: #777e78;
  white-space: nowrap;
}

.travel-number {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 360px;
}

.travel-control {
  height: 52px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #f8f9f7;
}

.travel-control:focus-within {
  border-color: #708278;
  outline: 3px solid #dfe7e1;
}

.travel-control input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  background-color :transparent;
  font: inherit;
}

.number-unit {
  color: #777e78;
  white-space: nowrap;
}

.requirements-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.field-hint {
  color: #8a908b;
  font-size: 14px;
}

.textarea-control {
  padding: 16px;
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #f8f9f7;
}

.textarea-control:focus-within {
  border-color: #708278;
  outline: 3px solid #dfe7e1;
}

.textarea-control textarea {
  width: 100%;
  min-height: 120px;
  padding: 0;
  border: 0;
  outline: 0;
  resize: vertical;
  background-color: transparent;
  color: #303530;
  font: inherit;
  line-height: 1.7;
}

.textarea-footer {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 12px;
  color: #9a9f9b;
  font-size: 13px;
}

.character-count {
  flex-shrink: 0;
  white-space: nowrap;
}

.character-count.is-near-limit {
  color: #b42318;
}

.submit-button {
  width: 100%;
  min-height: 60px;
  padding: 0 24px;
  border: 0;
  border-radius: 14px;
  background-color: #303530;
  color: #ffffff;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #252925;
}

.submit-button:focus-visible {
  outline: 3px solid #aebdb3;
  outline-offset: 3px;
}

.submit-button:disabled {
  background-color: #dfe3de;
  color: #8a908b;
  cursor: not-allowed;
}

.submission-preview {
  margin-top: 24px;
  padding: 20px;
  border: 1px solid #dfe3dc;
  border-radius: 12px;
  background-color: #f8f9f7;
}

.submission-preview h3 {
  margin-top: 0;
}

.submission-preview pre {
  margin-bottom: 0;
  overflow-x: auto;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.button-content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.button-arrow {
  flex-shrink: 0;
  transition: transform 200ms ease;
}

.submit-button.is-result-button:hover .button-arrow {
  transform: translateX(3px);
}

.submit-button.is-result-button {
  background-color: #708278;
}

.submit-button.is-result-button:hover {
  background-color: #607269;
}


.required-hint {
  margin-left: 8px;
  color: #8a908b;
  font-size: 13px;
  font-weight: 400;
}

.work-progress {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.progress-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  color: #747b75;
}

.progress-heading strong {
  flex-shrink: 0;
  color: #657b6d;
}

.progress-track {
  width: 100%;
  height: 6px;
  overflow: hidden;
  border-radius: 999px;
  background-color: #e5e8e3;
}

.progress-fill {
  width: 0;
  height: 100%;
  border-radius: inherit;
  background-color: #708278;
  transition: width 300ms ease;
}

.progress-estimate {
  margin: 0;
  color: #9a9f9b;
  font-size: 13px;
  text-align: center;
}

.planning-card {
  /*margin-top: 24px;*/
  padding: 28px;
  border: 1px solid #e1e4de;
  border-radius: 20px;
  background-color: #ffffff;
}

.planning-card > h2 {
  margin: 0;
  font-size: 16px;
  color: #657b6d;
}

.stage-list {
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin: 28px 0 0;
  padding: 0;
  list-style: none;
}

.stage-item {
  display: grid;
  grid-template-columns: 30px 1fr;
  gap: 12px;
  color: #9a9f9b;
}

.stage-marker {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border: 2px solid #c9cec9;
  border-radius: 50%;
  color: #8d948e;
  font-size: 14px;
  font-weight: 700;
}

.stage-copy h3 {
  margin: 2px 0 4px;
  color: inherit;
  font-size: 15px;
}

.stage-copy p {
  margin: 0;
  color: inherit;
  font-size: 13px;
  line-height: 1.5;
}

.stage-item.is-completed {
  color: #657b6d;
}

.stage-item.is-completed .stage-marker {
  border-color: #b8c8bc;
  background-color: #edf2ed;
  color: #657b6d;
}

.stage-item.is-active {
  color: #303530;
}

.stage-item.is-active .stage-marker {
  border-color: #708278;
  background-color: #edf2ed;
  color: #657b6d;
}

.stage-item.is-pending {
  color: #a3a8a4;
}

.planner-layout {
  display: grid;
  grid-template-columns:
    minmax(0, 2fr)
    minmax(300px, 1fr);
  gap: 24px;
  align-items: start;
  margin-top: 32px;
}

.circular-progress {
  position: relative;
  width: 116px;
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  margin-top: 0;
  flex: 0 0 116px;
  border-radius: 50%;
}

.circular-progress::before {
  content: '';
  position: absolute;
  inset: 7px;
  border-radius: 50%;
  background-color: #ffffff;
}

.circular-progress span {
  position: relative;
  z-index: 1;
  color: #303530;
  font-size: 28px;
  font-weight: 600;
}

@media (max-width: 900px) {
  .planner-layout {
    grid-template-columns: 1fr;
  }
}

.planning-overview {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 28px;
  padding-bottom: 28px;
  border-bottom: 1px solid #e5e8e3;
}

.planning-overview-copy {
  min-width: 0;
}

.planning-overview-copy h3 {
  margin: 0;
  color: #303530;
  font-size: 18px;
}

.planning-overview-copy p {
  margin: 8px 0 0;
  color: #8a908b;
  font-size: 13px;
  line-height: 1.5;
}

.completion-summary {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.completion-check {
  width: 64px;
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background-color: #edf2ed;
  color: #657b6d;
  font-size: 28px;
}

.completion-summary h2 {
  margin: 8px 0 0;
  color: #303530;
  font-size: 24px;
}

.completion-summary > p {
  margin: 0;
  color: #7d847e;
  line-height: 1.7;
}

.completion-stats {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(
    3,
    minmax(0, 1fr)
  );
  gap: 12px;
  padding: 20px;
  border-radius: 14px;
  background-color: #f7f8f6;
}

.completion-stat {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.completion-stat strong {
  color: #303530;
  font-size: 18px;
  white-space: nowrap;
}

.completion-stat span {
  color: #8a908b;
  font-size: 12px;
}

.completion-highlights {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
}

.completion-highlight {
  display: grid;
  grid-template-columns: 22px 1fr;
  gap: 10px;
  align-items: start;
  color: #6f766f;
  font-size: 14px;
  line-height: 1.6;
}

.highlight-check {
  width: 20px;
  height: 20px;
  display: grid;
  place-items: center;
  margin-top: 1px;
  border: 1px solid #87988d;
  border-radius: 50%;
  color: #657b6d;
  font-size: 12px;
  font-weight: 700;
}

.submit-button.is-result-button {
  background-color: #708278;
}

.submit-button.is-result-button:hover {
  background-color: #607269;
}

@media (max-width: 900px) {
  /* 标题和步骤条改为上下排列 */
  .page-top {
    flex-direction: column;
    align-items: stretch;
  }

  /* 步骤太宽时允许横向滚动，不挤坏文字 */
  .page-stepper {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .step-list {
    min-width: max-content;
  }

  /* 主页面由左右两栏变为单栏 */
  .planner-layout {
    grid-template-columns: 1fr;
  }

  /* 单栏时限制日历宽度，避免日期格子变得过大 */
  .calendar-card {
    width: 100%;
    max-width: 520px;
    align-self: center;
  }
}

@media (max-width: 520px) {
  .planner-page {
    padding: 16px;
  }

  .preference-card,
  .calendar-card,
  .planning-card {
    padding: 20px;
    border-radius: 16px;
  }

  .calendar-navigation {
    grid-template-columns: 36px 1fr 36px;
    margin-top: 18px;
  }

  .calendar-nav-button {
    width: 36px;
    height: 36px;
  }

  .calendar-day {
    border-radius: 8px;
    font-size: 13px;
  }

  .calendar-summary {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>










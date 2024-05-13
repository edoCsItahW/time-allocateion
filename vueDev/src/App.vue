<script>
const date = new Date();
const weekList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', "Sun"];

let taskInitUI = null;
let start = null;
let end = null;
let taskName = null;

onload = () => {
    taskInitUI = document.getElementById("task-init-ui");
    start = document.getElementById("start-time")
    end = document.getElementById("end-time")
    taskName = document.getElementById("task-name")
}

export default {
    data() {
        return {
            weekKey: weekList,
            dayTable: weekList.reduce((obj, key) => {
                obj[key] = [];
                return obj
            }, {}),
            showTimeDiv: true,
            showTaskInitUI: false,
        }
    },
    methods: {
        addTask(event) {
            const week = event.target.getAttribute('week')

            if (taskInitUI) {
                this.showTaskInitUI = true;
                taskName.value = "";
            }

        },
        getTodayWeek() {
            return weekList[date.getDay()]
        },
    }
}
</script>

<template>
    <div class="task-init-ui" id="task-init-ui" v-show="showTaskInitUI">
        <svg class="close-icon" @click="showTaskInitUI = false" viewBox="0 0 20 20" width="24" height="24">
            <rect x="2" y="2" width="16" height="16" stroke="white" rx="2" ry="2" fill="#ccc"/>
            <line x1="4" y1="4" x2="16" y2="16" stroke="red" stroke-width="2"/>
            <line x1="16" y1="4" x2="4" y2="16" stroke="red" stroke-width="2"/>
        </svg>
        <div class="label-div">
            <label class="label-name" for="task-name">任务名:</label>
            <input class="task-input" type="text" id="task-name" placeholder="任务名">
        </div>
        <div class="label-div">
            <label class="label-name" for="constant">固定时段:</label>
            <input class="task-input" type="checkbox" id="constant" v-model="showTimeDiv">
        </div>
        <div class="label-div" v-if="showTimeDiv">
            <label class="label-name" for="start-time">开始时间:</label>
            <input class="task-input" type="time" id="start-time">
        </div>
        <div class="label-div" v-if="showTimeDiv">
            <label class="label-name" for="end-time">结束时间:</label>
            <input class="task-input" type="time" id="end-time">
        </div>
        <div class="label-div" v-if="!showTimeDiv">
            <label class="label-name" for="task-weight">任务权重:</label>
            <input class="task-input" type="number" id="task-weight" value="1.0" min="0" max="1.0">
        </div>

    </div>
    <div class="toolbar">
        <div class="label-container">
            <div class="dayLabel" v-for="text in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']">{{ text }}</div>
        </div>
        <div class="botton-container">
            <div class="add-botton" v-for="i in Array.from({length: 7}, (_, idx) => `${weekKey[idx]}`)" :week="i"
                 @click="addTask">+
            </div>
        </div>
    </div>
    <div class="container">
        <div class="day-serise" id="mon">
            <div class="task-list" v-for="elem in dayTable['mon']">{{ elem }}</div>
        </div>
        <div class="day-serise" id="tue"></div>
        <div class="day-serise" id="wed"></div>
        <div class="day-serise" id="thu"></div>
        <div class="day-serise" id="fri"></div>
        <div class="day-serise" id="sat"></div>
        <div class="day-serise" id="sun"></div>
    </div>
</template>

<style>
.close-icon {
    float: right;
}

.task-init-ui {
    position: absolute;
    top: 50%; /* 从顶部开始，偏移50%的父元素高度 */
    left: 50%; /* 从左侧开始，偏移50%的父元素宽度 */
    transform: translate(-50%, -50%); /* 相对于元素自身的中心点进行移动，以使其完全居中 */
    width: 50%;
    height: 50%;
    border-radius: 5px;
    background-color: #1f2024;
    z-index: 1;
    flex-direction: column;
}

.label-name {
    color: #ccc;
    font-size: 100%;
    margin: 0 2%;
}

.task-input {
    border-radius: 5px;
    background-color: rgba(255, 255, 255, 0.04);
    color: #ccc;
}

.toolbar {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.label-container {
    width: 100%;
    display: flex;
    flex-direction: row;
}

.botton-container {
    width: 100%;
    display: flex;
    flex-direction: row;
}

.dayLabel {
    width: 100%;
    text-align: center;
    margin: 0 4px;
}

.add-botton {
    width: 100%;
    text-align: center;
    border-radius: 5px;
    border: 2px solid rgba(151, 151, 151, 0.38);
    margin: 2px;
    background-color: rgba(193, 192, 192, 0.38);
}

.container {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: row;
}

.day-serise {
    width: 100%;
    border-radius: 5px;
    border: 2px solid #0075FBFF;
    margin: 2px;
}

</style>

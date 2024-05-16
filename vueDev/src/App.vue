<script>
import { elemOption, $ } from "jsPackage/src/commonlyFunc/index.js"
// npm install in path


const date = new Date();
const weekList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', "Sun"];

let taskInitUI = null;
let taskName = null;
let taskContainter = null;
let bottonContainer = null;

onload = () => {
    taskInitUI = $.id("task-init-ui");
    taskName = $.id("task-name");
    bottonContainer = $.class("botton-container")
    taskContainter = $.class("task-container");
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
            allocTasks: [],
        }
    },
    methods: {
        openUi(event) {
            const week = event.target.getAttribute('week')

            if (taskInitUI) {
                this.showTaskInitUI = true;
                taskName.value = "";
            }

        },
        addFixedTask(status) {
            // TODO: 实现固定任务的添加
        },
        addVarTask(status) {
            this.allocTasks.push(status);
            if (taskContainter.getBoundingClientRect().width > 0.75 *  bottonContainer.getBoundingClientRect().width) {
                taskContainter.style.minWidth = taskContainter.getBoundingClientRect().width + "px";
                taskContainter.style.overflowX = "auto";
                taskContainter.style.overflowY = "hidden";
            }
        },
        addTask(status) {
            if (status['fixed']) this.addFixedTask(status);
            else this.addVarTask(status);
        },
        calcuWeight() {

        },
        submitTask(event) {

            let taskStatus = {};

            if (!taskName.value) {
                alert("请输入任务名!");
                return;
            }

            for (let elem of elemOption.findTag(taskInitUI, "input")) {
                let label = "";

                if (elem.hasAttribute("label")) {
                    label = elem.getAttribute("label");
                }
                else {
                    alert(`元素: '${elem}'没有设置标签!`);
                    return;
                }

                if (elem.type !== "submit") {
                    if (label === 'day' && !elem.value.match(/^(mon|tue|wed|thu|fri|sat|sun)$/)) {
                        alert("请输入正确的星期缩写单词!");

                        return;

                    }

                    taskStatus[elem.getAttribute("label")] = elem.type === "checkbox" ? elem.checked : elem.value;

                }

            }
            this.addTask(taskStatus);

            this.showTaskInitUI = false;

        }
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
            <input class="task-input" type="text" id="task-name" label="name" placeholder="任务名">
        </div>
        <div class="label-div">
            <label class="label-name" for="fixed">固定时段:</label>
            <input class="task-input" type="checkbox" id="fixed" label="fixed" v-model="showTimeDiv">
        </div>
        <div class="label-div" v-if="showTimeDiv">
            <label class="label-name" for="day">星期:</label>
            <input class="task-input" type="text" id="day" label="day" placeholder="mon|tue|wed|thu|fri|sat|sun" pattern="^(mon|tue|wed|thu|fri|sat|sun)$" required>
        </div>
        <div class="label-div" v-if="showTimeDiv">
            <label class="label-name" for="start-time">开始时间:</label>
            <input class="task-input" type="time" label="start" id="start-time">
        </div>
        <div class="label-div" v-if="showTimeDiv">
            <label class="label-name" for="end-time">结束时间:</label>
            <input class="task-input" type="time" label="end" id="end-time">
        </div>
        <div class="label-div" v-if="!showTimeDiv">
            <label class="label-name" for="task-weight">紧迫程度:</label>
            <input class="task-input" type="number" id="task-urgent" label="urgent" value="0" step="0.1" min="0" max="1.0">
        </div>
        <div class="label-div" v-if="!showTimeDiv">
            <label class="label-name" for="artif-time">干预权重:</label>
            <input class="task-input" type="number" id="artif-degree" label="artif" value="0" step="0.1" min="0" max="1.0">
        </div>
        <div class="label-div" v-if="!showTimeDiv">
            <label class="label-name" for="suit-time-start">尽量不早于:</label>
            <input class="task-input" type="time" id="suit-time-start" label="suitStart">
        </div>
        <div class="label-div" v-if="!showTimeDiv">
            <label class="label-name" for="suit-time-end">尽量不晚于:</label>
            <input class="task-input" type="time" id="suit-time-end" label="suitEnd">
        </div>

        <input class="confirm-btn" type="submit" value="确认" label="config" @click="submitTask">

    </div>
    <div class="toolbar">
        <div class="label-container">
            <div class="dayLabel" v-for="text in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']">{{ text }}</div>
        </div>
        <div class="botton-container">
            <div class="task-container">
                <div class="alloc-task" v-for="(taskDict) in allocTasks">
                    <label class="task-label">待分配</label>
                    <label class="task-label">{{ taskDict['name'] }}</label>
                </div>
            </div>
            <div class="add-botton" @click="openUi">
                <svg viewBox="0 0" height="45">
                    <line x1="50%" y1="15%" x2="50%" y2="95%" stroke="black" stroke-width="5" stroke-linecap="round"></line>
                    <line x1="40%" y1="50%" x2="60%" y2="50%" stroke="black" stroke-width="5" stroke-linecap="round"></line>
                </svg>
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
body {
    background-color: #1f2024;
}

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

.task-container {
    max-width: 90%;
    padding: 1px 0 5px 0;
    display: flex;
    flex-direction: row;
}

.alloc-task {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    border: 2px solid #ccc;
    margin: 0 2px;
    background-color: #9aa0ff;
    min-width: 100px;
    display: flex;
    flex-direction: column;
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
    min-width: 10px;
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
    border: 2px solid #888888;
    margin: 2px;
}

</style>

## type (任务类型)

### Task (任务基类)
   > Task(ABC) {.class}

   1. name (任务名称)
       > name (str) {.attribute}

   2. start (任务开始时间)
       > start (time) {.attribute}  # abstractmethod

   3. end (任务结束时间)
       > end (time) {.attribute}  # abstractmethod

   4. duration (任务持续时间)
       > duration (int | float) {.attribute}  # final

   5. day (任务所在日/星期)
       > day (str) {.attribute}

   6. uuid (任务唯一标识符)
       > uuid (str) {.attribute}  # property

   7. type (任务类型)
       > type (str) {.attribute}  # property final
    
#### Fixed-time task (固定时间任务)
   > fixTask(Task) {.class}

   1. start (任务开始时间)
       > start (time) {.attribute}  # property
   
   2. end (任务结束时间)
       > end (time) {.attribute}  # property
   
#### Variable-time task (待定时间任务)
   > varTask(Task) {.class}

   1. start (任务开始时间)
       > start (time) {.attribute}  # property setter

   2. end (任务结束时间)
       > end (time) {.attribute}  # property setter

   3. wight (任务权重)
       > weight (int | float) {.attribute}  # property (0, 1.0)

### weekTable (星期表)
   > weekTable {.class}

   1. table (星期表)
       > table (dict[str, dict[str, list[task]]]) {.attribute}  # property

   2. dayStart (每日开始时间)
       > dayStart (time) {.attribute}  # property

   3. dayEnd (每日结束时间)
       > dayEnd (time) {.attribute}  # property

   4. readyAlloc (待分配任务列表)
       > readyAlloc (list[task]) {.attribute}  # property

   5. dayDuration (每日时长)
       > dayDuration (int | float) {.attribute}  # property

   * method (方法)

      1. addTask (添加任务)
         > addTask(task: Task) {.method}

         * 检查任务的类型
      
            * fixTask
            
               * 检查任务时长是否超出每日时长
                  
                  * 超出
                  
                     抛出异常
                 
                  * 不超出
                  
                     根据fixTask的day属性，将任务添加到星期表中对应的列表中
            
            * varTask
         
               * 直接添加到待分配列表中

      2. removeTask (移除任务)
         > removeTask(task: Task) {.method}

         在try-except中直接移除
     

### Allocate (任务分配)
   > Allocate {.class}

   1. weekTable (引用星期表)
       > weekTable (weekTable) {.attribute}  # property

   2. allocList (引用待分配表)
       > allocTable (list[task]) {.attribute}  # property

   * method (方法)

      1. allocate (分配任务)
         > allocate() {.method}
         
         * 遍历待分配列表，按照权重排序
         
         * 将总空闲时间根据权重和其特性分配到每一个varTask中,并更新任务的开始和结束时间
     
            * 如果任务时长大于某天的可用时长,则将任务分割为两个任务         
    
         * 遍历星期表，将varTask添加到对应的列表中
         
      2. accumFreeTime (累计空闲时间)
         > accumFreeTime() {.method}
      
         * 遍历星期表，计算每日空闲时间,并求和

### duration (时长封装)
   > duration {.class}

   1. seconds (秒)
       > seconds (int) {.attribute}  # property

   2. minutes (分)
       > minutes (int) {.attribute}  # property

   3. hours (时)
       > hours (int) {.attribute}  # property
      
   * method (方法)
      1. calcuTimeDuration (计算时长)
         > calcuTimeDuration(seconds: int) {.method}
         
         * 将两个time类型的时间差转换为duration类型的时间差
         

## Algorithm (算法)

### 关于一个任务 

1. 紧迫程度  # 越高分配到的时间就越多

2. 重要程度  # 越高分配到的时间就越多 

3. 适宜时间段  # 如果该值被设置,那么任务被分配到该时段的概率会更高

4. 

### 分配限制

1. 一个任务一天只能出现一次

2. 在一周之内不能每天都出现同一任务

3. 一天至少有两个任务

-- 随笔应用数据库设计
-- 创建数据库
CREATE DATABASE IF NOT EXISTS note_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE note_app;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
  `nickname` VARCHAR(50) NULL DEFAULT NULL COMMENT '昵称',
  `avatar` VARCHAR(255) NULL DEFAULT NULL COMMENT '头像URL',
  `gender` ENUM('male', 'female', 'unknown') NULL DEFAULT 'unknown' COMMENT '性别',
  `bio` VARCHAR(500) NULL DEFAULT NULL COMMENT '个人简介',
  `phone` VARCHAR(20) NULL DEFAULT NULL COMMENT '手机号',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 用户令牌表
CREATE TABLE IF NOT EXISTS `user_token` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '令牌ID',
  `user_id` INT UNSIGNED NOT NULL COMMENT '用户ID',
  `token` VARCHAR(255) NOT NULL COMMENT '令牌值',
  `expires_at` TIMESTAMP NOT NULL COMMENT '过期时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `token_UNIQUE` (`token` ASC),
  INDEX `fk_user_token_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_token_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户令牌表';

-- 随笔分类表
CREATE TABLE IF NOT EXISTS `note_category` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序顺序',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='随笔分类表';

-- 随笔表
CREATE TABLE IF NOT EXISTS `note` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '随笔ID',
  `title` VARCHAR(255) NOT NULL COMMENT '随笔标题',
  `description` VARCHAR(500) NULL DEFAULT NULL COMMENT '随笔简介',
  `content` TEXT NOT NULL COMMENT '随笔内容',
  `image` VARCHAR(255) NULL DEFAULT NULL COMMENT '封面图片URL',
  `author` VARCHAR(50) NULL DEFAULT NULL COMMENT '作者',
  `category_id` INT UNSIGNED NOT NULL COMMENT '分类ID',
  `views` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览量',
  `publish_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `fk_note_category_idx` (`category_id` ASC),
  INDEX `idx_publish_time` (`publish_time` DESC),
  CONSTRAINT `fk_note_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `note_category` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='随笔表';

-- 相关随笔关联表（推荐系统）
CREATE TABLE IF NOT EXISTS `related_note` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `note_id` INT UNSIGNED NOT NULL COMMENT '随笔ID',
  `related_note_id` INT UNSIGNED NOT NULL COMMENT '相关随笔ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `note_related_unique` (`note_id` ASC, `related_note_id` ASC),
  INDEX `fk_related_note_note_idx` (`note_id` ASC),
  INDEX `fk_related_note_related_idx` (`related_note_id` ASC),
  CONSTRAINT `fk_related_note_note`
    FOREIGN KEY (`note_id`)
    REFERENCES `note` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_related_note_related`
    FOREIGN KEY (`related_note_id`)
    REFERENCES `note` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='相关随笔关联表';

-- 收藏表
CREATE TABLE IF NOT EXISTS `favorite` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` INT UNSIGNED NOT NULL COMMENT '用户ID',
  `note_id` INT UNSIGNED NOT NULL COMMENT '随笔ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_note_unique` (`user_id` ASC, `note_id` ASC),
  INDEX `fk_favorite_user_idx` (`user_id` ASC),
  INDEX `fk_favorite_note_idx` (`note_id` ASC),
  CONSTRAINT `fk_favorite_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_favorite_note`
    FOREIGN KEY (`note_id`)
    REFERENCES `note` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收藏表';

-- 浏览历史表
CREATE TABLE IF NOT EXISTS `history` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '历史ID',
  `user_id` INT UNSIGNED NOT NULL COMMENT '用户ID',
  `note_id` INT UNSIGNED NOT NULL COMMENT '随笔ID',
  `view_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`),
  INDEX `fk_history_user_idx` (`user_id` ASC),
  INDEX `fk_history_note_idx` (`note_id` ASC),
  INDEX `idx_view_time` (`view_time` DESC),
  CONSTRAINT `fk_history_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_history_note`
    FOREIGN KEY (`note_id`)
    REFERENCES `note` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='浏览历史表';

-- AI聊天记录表（Agent）
CREATE TABLE IF NOT EXISTS `ai_chat` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '聊天记录ID',
  `user_id` INT UNSIGNED NOT NULL COMMENT '用户ID',
  `message` TEXT NOT NULL COMMENT '用户消息',
  `response` TEXT NOT NULL COMMENT 'AI回复',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `fk_ai_chat_user_idx` (`user_id` ASC),
  INDEX `idx_created_at` (`created_at` DESC),
  CONSTRAINT `fk_ai_chat_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI聊天记录表';

-- 初始化数据
-- 插入默认随笔分类
INSERT INTO `note_category` (`name`, `sort_order`) VALUES 
('推荐', 1),
('日常', 2),
('灵感', 3),
('阅读', 4),
('观影', 5),
('随笔', 6),
('收藏', 7),
('暗黑', 8);

-- 插入默认随笔
INSERT INTO `note` (`title`, `description`, `content`, `image`, `author`, `category_id`, `views`, `publish_time`) VALUES
('清晨窗边的一杯温水', '从一杯温水开始整理一天的节奏。', '早晨醒来时，窗帘缝里透进一条很细的光。我没有马上打开手机，而是先给自己倒了一杯温水。水汽慢慢升起来，房间里的声音也一点点清晰。原来一天不必从催促开始，也可以从安静里醒来。把桌面收拾干净，给绿植浇水，再写下今天最重要的一件事，心里就有了方向。', 'https://picsum.photos/id/10/200/200', '林小满', 1, 1280, '2026-01-02 08:10:00'),
('雨天适合把脚步放慢', '雨声让城市短暂降噪，也让人重新听见自己。', '下雨的下午，街边的树叶被洗得发亮。公交车开过时溅起一小片水花，行人撑着伞从容地走。平时总觉得时间不够用，雨天却像把钟表调慢了一格。我坐在窗边读完了搁置很久的几页书，也认真回了一封旧邮件。很多事情不是没时间，只是我们太习惯把注意力交给热闹。', 'https://picsum.photos/id/11/200/200', '周闻笛', 1, 960, '2026-01-04 15:30:00'),
('给书桌留一块空白', '空白不是浪费，而是让思绪有地方停靠。', '以前我的书桌总是堆满纸张、数据线和临时放下的小物件，像一片没有尽头的待办清单。后来我刻意留出右上角的一块空白，只放一盏台灯。奇怪的是，这个小小的空位让我更愿意坐下来写东西。空间会影响情绪，情绪又决定我们如何面对生活。整理桌面，其实也是在整理心里的拥挤。', 'https://picsum.photos/id/12/200/200', '许知行', 2, 1420, '2026-01-06 20:20:00'),
('旧相册里的夏天', '翻到泛黄照片时，记忆忽然有了温度。', '周末整理柜子，翻出一本很旧的相册。照片里的夏天总是明亮，院子里的葡萄架、搪瓷盆里的西瓜、傍晚摇着蒲扇的大人，都带着缓慢的气息。那时我们不知道什么叫记录生活，只是自然地生活着。现在照片越来越多，真正被记住的瞬间却不一定更多。也许珍贵的不是影像，而是当时愿意停下来的心。', 'https://picsum.photos/id/13/200/200', '沈南枝', 2, 1760, '2026-01-08 19:45:00'),
('晚饭后的散步路线', '熟悉的小路也会在不同心情里长出新风景。', '吃过晚饭，我习惯沿着小区外的河边走一圈。路线不长，刚好够消化一顿饭，也够把白天的杂念放下。桥下有人练萨克斯，便利店门口的灯牌一闪一闪，遛弯的老人慢慢聊着家常。生活的安稳常常不在大事里，而在这些每天重复的小片段里。走到第三棵梧桐树时，我通常就原谅了今天的不完美。', 'https://picsum.photos/id/14/200/200', '陈予安', 3, 2310, '2026-01-10 21:05:00'),
('把周末还给自己', '不安排过满，也是一种认真生活。', '过去我总想把周末安排得很有效率，洗衣、采购、见朋友、学习、整理资料，一件接一件。结果到了周日晚上，反而比工作日更疲惫。后来我开始给周末留半天没有计划的时间。可以睡个午觉，也可以随便出门走走。真正的休息不是停止行动，而是不再被必须完成的清单推着走。', 'https://picsum.photos/id/15/200/200', '顾清禾', 3, 1880, '2026-01-12 10:25:00'),
('一封没有寄出的信', '写信的过程，有时比送达更重要。', '我曾经写过一封很长的信，写给多年没有联系的朋友。写完后没有寄出，只把它夹在书里。后来再读，才发现那封信真正想说的不是责备，也不是怀念，而是和过去的自己握手言和。有些话说出口会打扰别人，写下来却能安放自己。信没有寄出，但它完成了自己的使命。', 'https://picsum.photos/id/16/200/200', '叶听澜', 4, 1190, '2026-01-14 22:10:00'),
('厨房里的小秩序', '锅碗瓢盆之间，也藏着生活的耐心。', '做饭前把食材一一摆好，是我最近学会的小习惯。番茄切块，鸡蛋打散，葱花放在小碟里，锅热后动作就不再慌乱。厨房教会人的不是厨艺本身，而是顺序和等待。火候急不得，调味也要慢慢试。很多关系、计划和愿望，大概也需要这样的耐心：先准备好，再交给时间。', 'https://picsum.photos/id/17/200/200', '陆星河', 4, 1540, '2026-01-16 18:35:00'),
('地铁上的观察笔记', '人群匆忙，但每个人都带着自己的故事。', '早高峰的地铁里，大家都低头看屏幕。有人背单词，有人改方案，有人抱着花，也有人靠着扶手补觉。车厢像一条移动的河，把不同的人短暂地放在一起。我喜欢在这样的时刻观察生活：一个孩子把座位让给老人，一个上班族悄悄擦掉眼角的泪。城市很大，但温柔并不罕见。', 'https://picsum.photos/id/18/200/200', '韩若水', 5, 2030, '2026-01-18 08:50:00'),
('慢慢学会拒绝', '边界感不是冷漠，而是对彼此负责。', '以前我很怕拒绝别人，总担心一句“不方便”会让关系变差。于是答应了很多超出能力的事，也在心里积累了许多疲惫。后来才明白，清楚表达自己的边界，是成年人关系里很重要的诚实。拒绝并不意味着不在乎，而是避免带着委屈勉强应付。真正稳定的关系，经得起坦白。', 'https://picsum.photos/id/19/200/200', '罗云舒', 5, 1670, '2026-01-20 13:15:00'),
('一本书读到一半也很好', '阅读不必总是完成任务，留下回声也算收获。', '书架上有几本只读到一半的书，过去我总觉得它们像未完成的作业。后来想想，那些读过的章节已经在某些时刻帮过我，未读完也并不遗憾。阅读不是打卡，也不是收集完成数。有些书适合一口气读完，有些书适合在不同年纪反复翻开。人与书相遇，也讲究时机。', 'https://picsum.photos/id/20/200/200', '白鹭洲', 6, 920, '2026-01-22 16:40:00'),
('黄昏时分的便利店', '小小店铺收纳了许多普通人的疲惫与慰藉。', '下班路上经过便利店，玻璃门一开，热柜里的关东煮冒着白气。有人买便当，有人取快递，有人只是进来躲一会儿风。便利店像城市夜晚的临时客厅，不问来处，也不催归途。我买了一瓶酸奶和一个饭团，坐在窗边看天色暗下去。平凡日子里的安慰，常常价格不高，却很及时。', 'https://picsum.photos/id/21/200/200', '江以宁', 6, 2110, '2026-01-24 19:10:00'),
('和父母聊天的耐心', '很多关心藏在重复的问题里。', '母亲打电话时总会问我吃饭没有、天气冷不冷、工作忙不忙。年轻时觉得这些问题重复，现在却听出了里面的牵挂。父母表达爱的方式有时很笨拙，像一件旧毛衣，不够新潮，却一直保暖。我也开始学着多说几句，不急着挂断。成年以后，耐心地回应家人，也是一种慢慢补上的温柔。', 'https://picsum.photos/id/22/200/200', '唐晚晴', 7, 2480, '2026-01-26 20:55:00'),
('搬家时留下的东西', '取舍之间，才知道什么真正陪伴过自己。', '搬家最难的不是打包，而是决定哪些东西不再带走。旧票根、坏掉的耳机、用完一半的笔记本，每一样都像在提醒某段时间的自己。最后我只留下常用的杯子、几本书和一张合照。生活向前走时，不必把所有证明都背在身上。能轻一点出发，也是一种成长。', 'https://picsum.photos/id/23/200/200', '宋知夏', 7, 1360, '2026-01-28 11:30:00'),
('给植物换盆的下午', '照顾一株植物，也是在练习照顾生活。', '阳台上的绿萝长得太密，我给它换了一个大一点的盆。松土、修根、添新土，看似简单，却需要小心。植物不会说话，但会用叶子的颜色回应照料。人也是这样，环境合适一点，水分充足一点，就能慢慢恢复生机。那个下午，我没有做什么大事，却觉得生活被重新扶正了一点。', 'https://picsum.photos/id/24/200/200', '林栖迟', 8, 1740, '2026-01-30 15:05:00'),
('深夜写下三件好事', '用很小的记录，对抗一天里的消耗。', '睡前我会写下今天发生的三件好事。有时只是早餐的豆浆很热，同事帮忙带了一份资料，回家路上刚好赶上绿灯。起初觉得这些事太小，不值得记录。坚持一段时间后才发现，生活并不是缺少好事，而是我们太容易让坏情绪占满视线。记录不是粉饰现实，而是给自己留一盏灯。', 'https://picsum.photos/id/25/200/200', '闻人月', 8, 2250, '2026-02-01 23:20:00'),
('城市角落的花店', '花不解决问题，但能提醒人继续热爱。', '转角新开了一家花店，门口摆着向日葵和洋桔梗。老板说，买花的人不一定都在庆祝，也有人只是想让房间亮一点。我买了一小束白色雏菊，插在透明杯子里。它当然不能解决工作压力，也不能改变天气，但它让餐桌变得柔软。生活需要一些无用却美好的东西，提醒我们不只是为了完成任务而活。', 'https://picsum.photos/id/26/200/200', '苏明净', 1, 1980, '2026-02-03 17:25:00'),
('第一次独自旅行', '一个人出发，才听见心里的声音。', '第一次独自旅行时，我把行程安排得很松。没有必须打卡的景点，也没有同行者的期待。早上在陌生城市的小店吃面，下午沿着河边走到天黑。一个人的旅途会放大不安，也会放大自由。原来我可以自己决定方向，自己处理小麻烦，也可以在迷路时停下来喝杯咖啡。那次旅行让我更相信自己。', 'https://picsum.photos/id/27/200/200', '孟微澜', 2, 2630, '2026-02-05 09:40:00'),
('关于早睡的失败练习', '改变习惯从来不是一句决心那么简单。', '我很多次计划早睡，结果总在睡前刷手机刷到很晚。后来不再只责怪自控力，而是把充电器放到客厅，睡前半小时把手机留在门外。习惯需要具体的环境帮忙，而不是空泛的口号。虽然偶尔还是会失败，但至少我知道自己正在练习。生活里的改变，大多不是突然变好，而是慢慢少错几次。', 'https://picsum.photos/id/28/200/200', '贺兰舟', 3, 1470, '2026-02-07 22:45:00'),
('把今天认真收尾', '结束一天的方式，会影响明天的开始。', '晚上关电脑前，我会花十分钟整理明天要做的事。把杯子洗干净，把桌面清空，把没完成的任务写到纸上。这样做不是为了显得自律，而是让大脑知道今天可以结束了。很多焦虑来自悬而未决，很多轻松来自清楚安放。认真收尾，是给明天的自己留下一条比较平坦的路。', 'https://picsum.photos/id/29/200/200', '秦时雨', 4, 1860, '2026-02-09 21:35:00');
-- 创建测试用户
INSERT INTO `user` (`username`, `password`, `nickname`, `gender`, `bio`) VALUES 
('admin', '$2b$12$TKevPbXcGL6Q1WdaFKbLhuueBuLfLyhkdk/0ESBvBv7X74.rNwiNm', '测试用户', 'unknown', '这是一个测试账号');
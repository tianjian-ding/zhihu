commit;
use zhihu;
CREATE TABLE `hotboard` (
  `recordId` int(11) NOT NULL AUTO_INCREMENT,
  `currentTime` varchar(20) NOT NULL,
  `questionId` varchar(20) NOT NULL,
  `answersNumber` varchar(10) NOT NULL,
  `hotValue` varchar(10) NOT NULL,
  `keywords` varchar(200) NOT NULL,
  `commentsNumber` varchar(10) NOT NULL,
  `createdTime` varchar(20) NOT NULL,
  `modifiedTime` varchar(20) NOT NULL,
  `followersNumber` varchar(10) NOT NULL,
  `visitNumber` varchar(10) NOT NULL,
  PRIMARY KEY (`recordId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `questions_title` (
  `questionId` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `questionTitle` varchar(200) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`questionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `answers_content` (
  `answerId` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `answerContent` mediumtext CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`answerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `answers` (
  `recordId` int(11) NOT NULL AUTO_INCREMENT,
  `currentTime` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `answerId` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `questionId` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `createdTime` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `updateTime` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `authorName` varchar(40) CHARACTER SET utf8mb4 NOT NULL,
  `authorGender` varchar(10) CHARACTER SET utf8mb4 NOT NULL,
  `voteUpNumber` varchar(10) CHARACTER SET utf8mb4 NOT NULL,
  `commentsNumber` varchar(10) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`recordId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


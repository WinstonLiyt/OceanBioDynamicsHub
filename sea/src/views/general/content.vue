<template>
  <div class="forum-detail">
    <!-- 帖子标题 -->
    <h1 class="post-title">{{ post.title }}</h1>

    <!-- 表格 -->
    <el-table :data="comments" border style="width: 100%">
      <el-table-column label="用户信息" prop="userInfo">
        <template #default="{ row }">
          <div>{{ row.userInfo }}</div>
        </template>
      </el-table-column>
      <el-table-column label="内容及评论" prop="content">
        <template #default="{ row }">
          <div>{{ row.content }}</div>
          <div v-for="(comment, index) in row.comments" :key="index">
            <div>{{ comment.user }}: {{ comment.comment }}</div>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination v-model:currentPage="currentPage" :page-size="pageSize" :total="totalComments"
      layout="prev, pager, next" @current-change="handlePageChange" />

    <!-- 发表评论 -->
    <div class="comment-submit">发表评论：</div>
    <el-input v-model="newComment" type="textarea" :rows="5" placeholder="请输入评论内容" class="comment-input"></el-input>
    <el-button type="primary" @click="submitComment">发表</el-button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  data() {
    return {
      post: {
        title: '帖子标题',
        // 其他帖子信息...
      },
      comments: [
        {
          userInfo: '用户信息1',
          content: '帖子内容1',
          comments: [{ user: '用户1', comment: '评论1' }, { user: '用户2', comment: '评论2' }]
        },
        {
          userInfo: '用户信息2',
          content: '帖子内容2',
          comments: [{ user: '用户3', comment: '评论3' }, { user: '用户4', comment: '评论4' }]
        }
        // 其他评论信息...
      ],
      totalComments: 20, // 总评论数
      pageSize: 5, // 每页显示评论数
      currentPage: 1, // 当前页码
      newComment: '' // 新评论内容
    };
  },
  methods: {
    handlePageChange(page) {
      this.currentPage = page;
    },
    submitComment() {
      console.log('新评论：', this.newComment);
      // 提交评论的逻辑处理
      this.newComment = ''; // 清空输入框
    }
  }
};
</script>

<style scoped>
.forum-detail {
  padding: 20px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.comment-submit {
  margin-top: 20px;
  font-weight: bold;
}

.comment-input {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>

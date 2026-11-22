<script setup lang="ts">
const props = defineProps<{
  resultId: string
}>()
</script>

<template>
    <main class="result-page">
        <header class="result-header">
            <h1>智能规划结果</h1>
            <p>路线替你想好了，沿途的风景留给你 喵~ </p>
        </header>

        <section class="result-placeholder">
            <h2>>杭州，刚刚好的两日慢游</h2>
            <p>完整行程内容将在这里显示。</p>
        </section>
    </main>
</template>

<style scoped>
.result-page {
    width: 100%;
    max-width: 1440px;
    min-height: 100vh;
    margin: 0 auto;
    padding: 24px;
}

.result-header h1 {
    margin: 8px 0 0;
    color: #7d847e;
}

.result-placeholder {
  margin-top: 32px;
  padding: 28px;
  border: 1px solid #e1e4de;
  border-radius: 20px;
  background-color: #ffffff;
}

.result-placeholder h2 {
  margin: 0;
}

.result-placeholder p {
  margin: 12px 0 0;
  color: #7d847e;
}
</style>
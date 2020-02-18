<template>
  <footer class="footer">
      <div class="container">
          <span class="text-muted"> © {{ new Date().getFullYear() }}</span>
      </div>
  </footer>
</template>

<script>
    export default {
        name: "footer"
    }
</script>

<style scoped>
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
  line-height: 60px;
  /*background-color: #60c0f5;*/
  /*  background-color: #f5f5f5;*/
    background-color: #3e3e3e;
text-align: center;
}
.container {
  width: auto;
  max-width: 680px;
  padding: 0 15px;
}
</style>

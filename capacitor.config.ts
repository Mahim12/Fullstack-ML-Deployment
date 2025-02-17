import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.example.helloworld',
  appName: 'hello-world-ionic',
  webDir: 'dist/hello-world-ionic/browser', // <-- Set to your Angular build output
};

export default config;

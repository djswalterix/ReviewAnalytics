import "@mantine/core/styles.css";
import {
  MantineProvider,
  AppShell,
  NavLink,
  Burger,
  Group,
  Title,
  createTheme,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
  useLocation,
} from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import PredictPage from "./pages/PredictPage";

const theme = createTheme({
  primaryColor: "orange",
  fontFamily:
    "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
  headings: {
    fontFamily:
      "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
    fontWeight: "700",
  },
  defaultRadius: "md",
  colors: {
    orange: [
      "#fff4e6",
      "#ffe8cc",
      "#ffd8a8",
      "#ffc078",
      "#ffa94d",
      "#ff922b",
      "#fd7e14",
      "#e8590c",
      "#d9480f",
      "#c92a05",
    ],
  },
});

function Shell() {
  const navigate = useNavigate();
  const location = useLocation();
  const [opened, { toggle, close }] = useDisclosure();

  const handleNav = (path: string) => {
    navigate(path);
    close();
  };

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 240,
        breakpoint: "sm",
        collapsed: { mobile: !opened },
      }}
      padding="md"
    >
      <AppShell.Header
        style={{
          backgroundColor: "white",
          borderBottom: "1px solid var(--mantine-color-gray-2)",
        }}
      >
        <Group h="100%" px="md">
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Title order={4} style={{ letterSpacing: -0.5 }}>
            ReviewAnalytics
          </Title>
          <Text size="xs" c="dimmed" ml={-4}>
            NLP Dashboard
          </Text>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar
        p="sm"
        style={{ borderRight: "1px solid var(--mantine-color-gray-2)" }}
      >
        <NavLink
          label="Dashboard"
          active={location.pathname === "/"}
          onClick={() => handleNav("/")}
          color="orange"
          variant="light"
          style={{ borderRadius: 8, marginBottom: 4 }}
        />
        <NavLink
          label="Predizione"
          active={location.pathname === "/predict"}
          onClick={() => handleNav("/predict")}
          color="orange"
          variant="light"
          style={{ borderRadius: 8 }}
        />
      </AppShell.Navbar>
      <AppShell.Main bg="gray.0">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/predict" element={<PredictPage />} />
        </Routes>
      </AppShell.Main>
    </AppShell>
  );
}

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <BrowserRouter>
        <Shell />
      </BrowserRouter>
    </MantineProvider>
  );
}

import "@mantine/core/styles.css";
import {
  MantineProvider,
  AppShell,
  NavLink,
  Burger,
  Group,
  Title,
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
      header={{ height: 56 }}
      navbar={{
        width: 220,
        breakpoint: "sm",
        collapsed: { mobile: !opened },
      }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Title order={4}>ReviewAnalytics</Title>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="md">
        <NavLink
          label="Dashboard"
          active={location.pathname === "/"}
          onClick={() => handleNav("/")}
        />
        <NavLink
          label="Predizione"
          active={location.pathname === "/predict"}
          onClick={() => handleNav("/predict")}
        />
      </AppShell.Navbar>
      <AppShell.Main>
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
    <MantineProvider>
      <BrowserRouter>
        <Shell />
      </BrowserRouter>
    </MantineProvider>
  );
}

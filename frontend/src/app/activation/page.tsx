import ArchiveShell from "@/components/archive-shell";
import ActivationForm from "@/components/activation-form";
import LogoutButton from "@/components/logout-button";

export default function ActivationPage() {
  return (
    <ArchiveShell compact>
      <ActivationForm />
      <LogoutButton />
    </ArchiveShell>
  );
}

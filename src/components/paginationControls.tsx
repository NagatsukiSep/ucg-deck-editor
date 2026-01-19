"use client";

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
} from "@/components/ui/pagination";
import { useI18n } from "@/i18n/I18nProvider";

type Props = {
  currentPage: number;
  totalCount: number;
  perPage: number;
  onPageChange: (page: number) => void;
};

export const PaginationControls = ({
  currentPage,
  totalCount,
  perPage,
  onPageChange,
}: Props) => {
  const { t } = useI18n();
  const totalPages = Math.ceil(totalCount / perPage);

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={() => onPageChange(currentPage - 1)}
            label={t("pagination.previous")}
          />
        </PaginationItem>

        {currentPage > 1 && (
          <PaginationItem>
            <PaginationEllipsis label={t("pagination.more")} />
          </PaginationItem>
        )}

        {currentPage > 0 && (
          <PaginationItem>
            <PaginationLink onClick={() => onPageChange(currentPage - 1)}>
              {currentPage}
            </PaginationLink>
          </PaginationItem>
        )}

        <PaginationItem>
          <PaginationLink isActive>{currentPage + 1}</PaginationLink>
        </PaginationItem>

        {currentPage < totalPages - 1 && (
          <PaginationItem>
            <PaginationLink onClick={() => onPageChange(currentPage + 1)}>
              {currentPage + 2}
            </PaginationLink>
          </PaginationItem>
        )}

        {currentPage < totalPages - 2 && (
          <PaginationItem>
            <PaginationEllipsis label={t("pagination.more")} />
          </PaginationItem>
        )}

        <PaginationItem>
          <PaginationNext
            onClick={() => onPageChange(currentPage + 1)}
            label={t("pagination.next")}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

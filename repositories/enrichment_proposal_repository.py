import json

from datetime import datetime, timedelta, timezone

from pathlib import Path

from domains.skill_enrichment import (
    SkillEnrichmentProposal
)


class EnrichmentProposalRepository:
    """
    Handles persistence of skill enrichment proposals.

    Active proposals are stored in:

        data/enrichment_proposals.json

    Rejected proposals are moved to:

        data/rejected_enrichment_proposals.json

    A permanent audit record is also maintained in:

        data/enrichment_history.json

    Responsibilities:
        - Store active proposals
        - Retrieve proposals
        - Update proposal status
        - Remove active proposals
        - Archive rejected proposals
        - Archive completed proposals
        - Restore rejected proposals
        - Maintain 30-day rejected-proposal retention
    """

    REJECTED_RETENTION_DAYS = 30

    def __init__(
        self,
        path: str = "data/enrichment_proposals.json",
        rejected_path: str = (
            "data/rejected_enrichment_proposals.json"
        ),
        history_path: str = (
            "data/enrichment_history.json"
        ),
    ):

        self.path = Path(path)

        self.rejected_path = Path(
            rejected_path
        )

        self.history_path = Path(
            history_path
        )

        self._ensure_storage_exists()

        # Remove rejected records older than
        # the configured retention period.
        self._cleanup_expired_rejected()

    # ==================================================
    # SAVE
    # ==================================================

    def save(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Save a new active enrichment proposal.

        A proposal cannot be created if an active
        proposal with the same skill ID already exists.
        """

        proposals = self._load_active()

        for existing in proposals:

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                raise ValueError(
                    "An enrichment proposal already "
                    "exists for skill "
                    f"'{proposal.skill_id}'."
                )

        proposals.append(
            self._to_dict(proposal)
        )

        self._write_active(
            proposals
        )

        return proposal

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal | None:
        """
        Retrieve an active proposal by skill ID.
        """

        proposals = self._load_active()

        for proposal_data in proposals:

            if (
                proposal_data["skill_id"].lower()
                == skill_id.lower()
            ):

                return self._from_dict(
                    proposal_data
                )

        return None

    # ==================================================
    # GET PENDING
    # ==================================================

    def get_pending(
        self,
    ) -> list[SkillEnrichmentProposal]:
        """
        Return all active proposals currently
        waiting for human review.
        """

        proposals = self._load_active()

        return [

            self._from_dict(
                proposal
            )

            for proposal in proposals

            if proposal.get("status")
            == "pending_review"

        ]

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Update an existing active proposal.
        """

        proposals = self._load_active()

        for index, existing in enumerate(
            proposals
        ):

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                proposals[index] = (
                    self._to_dict(proposal)
                )

                self._write_active(
                    proposals
                )

                return proposal

        raise ValueError(
            "Enrichment proposal not found for "
            f"skill '{proposal.skill_id}'."
        )

    # ==================================================
    # DELETE ACTIVE
    # ==================================================

    def delete(
        self,
        skill_id: str,
    ) -> None:
        """
        Permanently remove a proposal from
        active proposal storage.

        This does NOT create an audit record.
        """

        proposals = self._load_active()

        updated_proposals = [

            proposal

            for proposal in proposals

            if proposal["skill_id"].lower()
            != skill_id.lower()

        ]

        if len(updated_proposals) == len(
            proposals
        ):

            raise ValueError(
                "Enrichment proposal not found "
                f"for skill '{skill_id}'."
            )

        self._write_active(
            updated_proposals
        )

    # ==================================================
    # REJECT + ARCHIVE
    # ==================================================

    def reject(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Reject an active proposal.

        Lifecycle:

            active proposal
                    ↓
                rejected
                    ↓
            rejected storage
                    +
              audit history

        The proposal is removed from active storage.
        """

        proposals = self._load_active()

        found = False

        updated_proposals = []

        for existing in proposals:

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                found = True

                rejected_data = (
                    self._to_dict(proposal)
                )

                rejected_data["status"] = (
                    "rejected"
                )

                rejected_data["rejected_at"] = (
                    self._utc_now()
                )

                self._save_rejected_record(
                    rejected_data
                )

                self._append_history(
                    rejected_data,
                    action="rejected",
                )

            else:

                updated_proposals.append(
                    existing
                )

        if not found:

            raise ValueError(
                "Enrichment proposal not found "
                f"for skill '{proposal.skill_id}'."
            )

        self._write_active(
            updated_proposals
        )

        proposal.status = "rejected"

        return proposal

    # ==================================================
    # ARCHIVE APPROVED
    # ==================================================

    def archive_approved(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> None:
        """
        Archive an approved proposal after it
        has successfully been applied to the
        Knowledge Base.

        The proposal is removed from active storage
        and permanently recorded in history.
        """

        proposals = self._load_active()

        found = False

        updated_proposals = []

        for existing in proposals:

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                found = True

                approved_data = (
                    self._to_dict(proposal)
                )

                approved_data["status"] = (
                    "approved"
                )

                approved_data["applied_at"] = (
                    self._utc_now()
                )

                self._append_history(
                    approved_data,
                    action="approved_and_applied",
                )

            else:

                updated_proposals.append(
                    existing
                )

        if not found:

            raise ValueError(
                "Enrichment proposal not found "
                f"for skill '{proposal.skill_id}'."
            )

        self._write_active(
            updated_proposals
        )

    # ==================================================
    # GET REJECTED
    # ==================================================

    def get_rejected(
        self,
    ) -> list[dict]:
        """
        Return rejected proposals still inside
        the 30-day recovery window.
        """

        self._cleanup_expired_rejected()

        return self._load_rejected()

    # ==================================================
    # GET REJECTED BY ID
    # ==================================================

    def get_rejected_by_skill(
        self,
        skill_id: str,
    ) -> dict | None:
        """
        Retrieve a rejected proposal from the
        recovery store.
        """

        self._cleanup_expired_rejected()

        rejected = self._load_rejected()

        for proposal in rejected:

            if (
                proposal["skill_id"].lower()
                == skill_id.lower()
            ):

                return proposal

        return None

    # ==================================================
    # RESTORE REJECTED
    # ==================================================

    def restore_rejected(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal:
        """
        Restore a rejected proposal back into
        active proposal storage.

        Restored proposal becomes:

            pending_review
        """

        self._cleanup_expired_rejected()

        rejected = self._load_rejected()

        target = None

        remaining = []

        for proposal in rejected:

            if (
                proposal["skill_id"].lower()
                == skill_id.lower()
            ):

                target = proposal

            else:

                remaining.append(
                    proposal
                )

        if target is None:

            raise ValueError(
                "Rejected proposal not found "
                f"for skill '{skill_id}'."
            )

        # Make sure an active proposal does not
        # already exist for this skill.
        existing = self.get(
            skill_id
        )

        if existing is not None:

            raise ValueError(
                "An active enrichment proposal "
                f"already exists for skill '{skill_id}'."
            )

        target["status"] = (
            "pending_review"
        )

        target.pop(
            "rejected_at",
            None
        )

        active_proposals = (
            self._load_active()
        )

        active_proposals.append(
            target
        )

        self._write_active(
            active_proposals
        )

        self._write_rejected(
            remaining
        )

        self._append_history(
            target,
            action="restored",
        )

        return self._from_dict(
            target
        )

    # ==================================================
    # HISTORY
    # ==================================================

    def get_history(
        self,
    ) -> list[dict]:
        """
        Return the permanent enrichment audit history.
        """

        return self._load_history()

    # ==================================================
    # ACTIVE STORAGE
    # ==================================================

    def _load_active(
        self,
    ) -> list[dict]:

        return self._load_json(
            self.path,
            "Enrichment proposal storage"
        )

    def _write_active(
        self,
        proposals: list[dict],
    ) -> None:

        self._write_json(
            self.path,
            proposals
        )

    # ==================================================
    # REJECTED STORAGE
    # ==================================================

    def _load_rejected(
        self,
    ) -> list[dict]:

        return self._load_json(
            self.rejected_path,
            "Rejected enrichment proposal storage"
        )

    def _write_rejected(
        self,
        proposals: list[dict],
    ) -> None:

        self._write_json(
            self.rejected_path,
            proposals
        )

    def _save_rejected_record(
        self,
        proposal: dict,
    ) -> None:
        """
        Append a rejected proposal to the
        rejected-proposal recovery storage.
        """

        rejected = self._load_rejected()

        rejected.append(
            proposal
        )

        self._write_rejected(
            rejected
        )

    # ==================================================
    # HISTORY STORAGE
    # ==================================================

    def _load_history(
        self,
    ) -> list[dict]:

        return self._load_json(
            self.history_path,
            "Enrichment history storage"
        )

    def _append_history(
        self,
        proposal: dict,
        action: str,
    ) -> None:
        """
        Append an immutable audit event.
        """

        history = self._load_history()

        record = dict(
            proposal
        )

        record["action"] = action

        record["recorded_at"] = (
            self._utc_now()
        )

        history.append(
            record
        )

        self._write_history(
            history
        )

    def _write_history(
        self,
        history: list[dict],
    ) -> None:

        self._write_json(
            self.history_path,
            history
        )

    # ==================================================
    # 30-DAY CLEANUP
    # ==================================================

    def _cleanup_expired_rejected(
        self,
    ) -> None:
        """
        Remove rejected proposals older than
        the configured recovery period.

        These records remain in permanent history.
        """

        rejected = self._load_rejected()

        cutoff = (
            datetime.now(
                timezone.utc
            )
            - timedelta(
                days=self.REJECTED_RETENTION_DAYS
            )
        )

        valid = []

        changed = False

        for proposal in rejected:

            rejected_at = (
                proposal.get(
                    "rejected_at"
                )
            )

            if not rejected_at:

                valid.append(
                    proposal
                )

                continue

            try:

                rejected_datetime = (
                    datetime.fromisoformat(
                        rejected_at
                    )
                )

            except ValueError:

                # Keep malformed timestamps rather
                # than accidentally deleting records.
                valid.append(
                    proposal
                )

                continue

            if rejected_datetime > cutoff:

                valid.append(
                    proposal
                )

            else:

                changed = True

        if changed:

            self._write_rejected(
                valid
            )

    # ==================================================
    # STORAGE HELPERS
    # ==================================================

    @staticmethod
    def _load_json(
        path: Path,
        description: str,
    ) -> list[dict]:

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                f"{description} contains "
                "invalid JSON."
            ) from error

        if not isinstance(
            data,
            list,
        ):

            raise RuntimeError(
                f"{description} must contain "
                "a JSON list."
            )

        return data

    @staticmethod
    def _write_json(
        path: Path,
        data: list[dict],
    ) -> None:

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def _ensure_storage_exists(
        self,
    ) -> None:
        """
        Create all required storage files.
        """

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        for path in (
            self.path,
            self.rejected_path,
            self.history_path,
        ):

            if not path.exists():

                self._write_json(
                    path,
                    []
                )

    # ==================================================
    # SERIALIZATION
    # ==================================================

    @staticmethod
    def _to_dict(
        proposal: SkillEnrichmentProposal,
    ) -> dict:
        """
        Convert a proposal domain object into
        JSON-compatible data.
        """

        return {

            "skill_id": proposal.skill_id,

            "name": proposal.name,

            "aliases": proposal.aliases,

            "category": proposal.category,

            "parent": proposal.parent,

            "related": proposal.related,

            "prerequisites": (
                proposal.prerequisites
            ),

            "unlocks": proposal.unlocks,

            "sources": proposal.sources,

            "confidence": proposal.confidence,

            "status": proposal.status,

        }

    # --------------------------------------------------

    @staticmethod
    def _from_dict(
        data: dict,
    ) -> SkillEnrichmentProposal:
        """
        Convert stored JSON data back into
        a SkillEnrichmentProposal.
        """

        return SkillEnrichmentProposal(

            skill_id=data["skill_id"],

            name=data["name"],

            aliases=data["aliases"],

            category=data["category"],

            parent=data["parent"],

            related=data["related"],

            prerequisites=data[
                "prerequisites"
            ],

            unlocks=data["unlocks"],

            sources=data["sources"],

            confidence=data["confidence"],

            status=data["status"],

        )

    # ==================================================
    # TIME
    # ==================================================

    @staticmethod
    def _utc_now() -> str:
        """
        Return a timezone-aware UTC timestamp
        in ISO-8601 format.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()
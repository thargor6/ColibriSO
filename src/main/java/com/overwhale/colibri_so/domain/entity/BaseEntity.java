package com.overwhale.colibri_so.domain.entity;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
public abstract class BaseEntity {
    @Id
    private UUID id;

    private OffsetDateTime creationTime;

    private OffsetDateTime lastChangedTime;

    private UUID creatorId;
}

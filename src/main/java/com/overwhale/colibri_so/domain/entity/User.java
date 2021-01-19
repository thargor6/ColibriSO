package com.overwhale.colibri_so.domain.entity;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
public class User {
  @Id
  private UUID id;

  private OffsetDateTime creationTime;

  private OffsetDateTime lastChangedTime;

  @NotNull
  private String username;

  private String email;

}
